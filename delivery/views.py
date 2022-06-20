

from urllib import response
from django.shortcuts import render,HttpResponse
from delivery import serializers
from delivery.models import additional_charges, currency_rate, delivery_rate,products,order_details
import enum
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from  delivery.serializers import order_Serializer
from rest_framework.decorators import api_view





# Create your views here.
"""class UserViewSet(APIView):
        def get(self,request):
                order_detail_view=order_details.objects.all()
                serializer=order_Serializer(order_detail_view,many=True)
                return response(serializer.data)
        def post(self):
                pass"""

@api_view(['GET'])
def api_view(request):
        order_detail=order_details.objects.all()
        serializer = order_Serializer(order_detail,many=True)
        return Response(serializer.data)

def home_page(request):
        products_row=products.objects.all()
        context={"products":products_row}
        return render(request,"home_page.html",context)

def second_page(request):
        
        #----------------------declaration and initialization of all variables-----------------------------

        selected_product_list=[]
        product_type_container=[]
        estimated_rate=0.0
        estimated_weight=0.0
        estimated_cost=0.0

        #-----------------------enum for charges_scheme_type------------------------------------
        class charges_scheme_type(enum.Enum):
                flat=0
                percentage=1
                per_kilo=2
        
        charges_in_flat=charges_scheme_type.flat.value
        charges_in_percentage=charges_scheme_type.percentage.value
        charges_in_perKilo=charges_scheme_type.per_kilo.value
        
        #-------------------------------enum for product_type(traditional,nontraditional)-----------------------------------------
        class product_type(enum.Enum):
                traditional=0
                non_traditional=1
        
        traditional_goods=product_type.traditional.value
        non_traditional_goods=product_type.non_traditional.value


        #-------------------------fetching all values from homepage's form using request.POST.get()------------------------------

        country=request.POST.get('parent')
        delivery_speed=request.POST.get('delivery_speed')
        height=request.POST.get('height')
        length=request.POST.get('length')
        weight=request.POST.get('weight')
        width=request.POST.get('width')
        state=request.POST.get('child')
        pickup_date_1=request.POST.get('pickup_date_1')
        pickup_date_2=request.POST.get('pickup_date_2')
        delivery_type=request.POST.get('delivery_type')
        selected_product_list.append(request.POST.getlist('goods_type'))

        
        #------------------------converting height,length and width string type to float for calculation-------------------

        height_float=float(height)
        length_float=float(length)    
        width_float=float(width)

        #---------------------------------calculating volumetric weight------------------------------------------------------------------- 

        volumetric_weight=(height_float*length_float*width_float)/5000
       

        #--------------------------fetching estimated_rate and estimated_weight for the particular volumetric_weight-----------------------------
        delivery_rate_row=delivery_rate.objects.raw('SELECT * FROM delivery_delivery_rate WHERE country = %s AND weight >= %s AND delivery_type=%s order by weight LIMIT 1;',[country,volumetric_weight,delivery_type])
        
    
        for elements in delivery_rate_row:
            estimated_rate=elements.amount
            estimated_weight=elements.weight
        

        #------------------------------------starting of calculation of total_cost of delivery--------------------------------------------

        #------------------------------estimation of weight charge and adding it to the delivery-cost----------------------------------------
        if(estimated_weight<=30):
                estimated_cost=estimated_rate
        elif(estimated_cost>30):
                estimated_cost=estimated_rate*volumetric_weight
        
        x1=estimated_cost
        
    

       
        #------------------------------estimation of covid charge and adding it to the delivery-cost-------------------------------------

        if country=='Australia'or country=='Newzeland':
                covid_charge=0.0
                estimated_cost=estimated_cost+covid_charge
        else:
                covid_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="COVID-CHARGE-SCHEME";')
                for elements in covid_charge_row:
                        if(elements.scheme_type==charges_in_flat):
                                estimated_cost=estimated_cost+elements.charge_per_transaction
                        elif(elements.scheme_type==charges_in_perKilo):
                                estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                        elif(elements.scheme_type==charges_in_percentage):
                                estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))
                           
        x2=estimated_cost
        #--------------------------estimation of fuel charge and adding it to the delivery-cost-----------------------------------------

        fuel_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="FUEL-CHARGE-SCHEME";')
        for elements in fuel_charge_row:
                if(elements.scheme_type==charges_in_flat):
                        estimated_cost=estimated_cost+elements.charge_per_transaction
                elif(elements.scheme_type==charges_in_perKilo):
                        estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                elif(elements.scheme_type==charges_in_percentage):
                        estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))
                        
                       
        x3=estimated_cost  
        #------------------estimation of heavy item charge and adding it to the delivery-cost-----------------------------------------     

        if volumetric_weight>40:
                heavy_item_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="HEAVY-ITEM-CHARGE-SCHEME(40+kg)";')

                for elements in heavy_item_charge_row:
                        if(elements.scheme_type==charges_in_flat):
                                estimated_cost=estimated_cost+elements.charge_per_transaction
                        elif(elements.scheme_type==charges_in_perKilo):
                                estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                        elif(elements.scheme_type==charges_in_percentage):
                                estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))
        
        x4=estimated_cost
        
        #----------------------estimation of pickup charge and adding it to the delivery-cost----------

        pickup_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="PICK-UP-CHARGE-SCHEME";')

        for elements in pickup_charge_row:
                if(elements.scheme_type==charges_in_flat):
                        estimated_cost=estimated_cost+elements.charge_per_transaction
                elif(elements.scheme_type==charges_in_perKilo):
                        estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                elif(elements.scheme_type==charges_in_percentage):
                        estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))
        

        
        x5=estimated_cost
        
       
        #-----------------finding if the non traditional items are included to customer's selected product list------------------------
        product_row=""
        product=""
        for selected_product in selected_product_list: 
              product_list=selected_product
              for i in range(len(product_list)):
                      product=product_list[i]
                      product_row=products.objects.raw('SELECT * FROM delivery_products WHERE product_name = %s;',[product])
                      for j in product_row:
                              product_type=j.product_type
                              product_type_container.append(product_type)

        if non_traditional_goods in product_type_container:
                product_type=non_traditional_goods 
                if volumetric_weight>10:
                        pickup_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="NON-TRADITIONAL-CAHRGE-SCHEME(10+kg)";')

                        for elements in pickup_charge_row:
                                if(elements.scheme_type==charges_in_flat):
                                        estimated_cost=estimated_cost+elements.charge_per_transaction
                                elif(elements.scheme_type==charges_in_perKilo):
                                        estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                                elif(elements.scheme_type==charges_in_percentage):
                                        estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))
        
                else:
                        pickup_charge_row=additional_charges.objects.raw('SELECT * FROM delivery_additional_charges WHERE scheme_name ="NON-TRADITIONAL-CAHRGE-SCHEME(upto-10kg)";')

                        for elements in pickup_charge_row:
                                if(elements.scheme_type==charges_in_flat):
                                        estimated_cost=estimated_cost+elements.charge_per_transaction
                                elif(elements.scheme_type==charges_in_perKilo):
                                        estimated_cost=estimated_cost+((elements.charge_per_transaction)*volumetric_weight)
                                elif(elements.scheme_type==charges_in_percentage):
                                        estimated_cost=estimated_cost+(estimated_cost*(elements.charge_per_transaction/100))                                       
        else:
                product_type=traditional_goods

        
        estimated_cost=round(estimated_cost,2)

        currency_rate_row=''

        currency_rate_row=currency_rate.objects.raw('SELECT * FROM delivery_currency_rate;')
        for rate in currency_rate_row:
                rate=rate.rate
        estimated_cost=(estimated_cost*rate)
        
       
        
        return render(request,"second_page.html",{"rate":rate,"x5":x5,"x1":x1,"x2":x2,"x3":x3,"x4":x4,"volumetric_weight":volumetric_weight,"estimated_cost":estimated_cost,"covid_charge_row":covid_charge_row,"product_type":product_type,"product_type_container":product_type_container,"product_row":product_row,"product":product,"product_list":product_list,"non_traditional_goods":non_traditional_goods,"traditional_goods":traditional_goods,"delivery_speed":delivery_speed,"height":height,"weight":weight,"width":width,"country":country,"state":state,"pickup_date_1":pickup_date_1,"pickup_date_2":pickup_date_2,"length":length,"delivery_type":delivery_type,"estimated_weight":estimated_weight})

    
       
       
       



    
    
def test_page(request):

        recipient_name=request.POST.get('recipient_name')
        phone=request.POST.get('phone')
        country=request.POST.get('country')
        state=request.POST.get('state')
        delivery_type=request.POST.get('delivery_type')
        house_number=request.POST.get('house_number')
        apartment_number=request.POST.get('apartment_number')
        town=request.POST.get('town')
        zip_code=request.POST.get('zip_code')
        street_name=request.POST.get('street_name')
        pickup_date_1=request.POST.get('pickup_date_1')
        pickup_date_2=request.POST.get('pickup_date_2')
        estimated_cost=request.POST.get('estimated_cost')
        product_list=request.POST.get('product_list')
        volumetric_weight=request.POST.get('volumetric_weight')
        estimated_weight=request.POST.get('estimated_weight')


        
        if request.method == 'POST':
                 order_details(recipient_name=recipient_name,phone=phone,country=country,state=state,town=town,house_number=house_number,street_name=street_name,apartment_number=apartment_number,
                 zip_code=zip_code,delivery_type=delivery_type,product_details=product_list,pickup_date_start=pickup_date_1,pickup_date_end=pickup_date_2,delivery_status="pending",estimated_weight=estimated_weight,
                 estimated_cost=estimated_cost,volumetric_weight=volumetric_weight).save()
               
        
              
        
       
        
        
 
    
        return render(request,"third_page.html",{"estimated_weight":estimated_weight,"volumetric_weight":volumetric_weight,"product_list":product_list,"pickup_date_1":pickup_date_1,"pickup_date_2":pickup_date_2,"estimated_cost":estimated_cost,"street_name":street_name,"house_number":house_number,"apartment_number":apartment_number,"town":town,"zip_code":zip_code,"delivery_type":delivery_type,"recipient_name":recipient_name,"phone":phone,"country":country,"state":state
        })



def third_page(request):

    #-------------------------fetching all values from secondpage's form using request.POST.get()------------------------------
       
        height=request.POST.get('height')
        width=request.POST.get('width')
        length=request.POST.get('length')
        weight=request.POST.get('weight')
        recipient_name=request.POST.get('recipient_name')
        phone=request.POST.get('phone')
        country=request.POST.get('country')
        state=request.POST.get('state')
        delivery_type=request.POST.get('delivery_type')
        house_number=request.POST.get('house_number')
        apartment_number=request.POST.get('apartment_number')
        town=request.POST.get('town')
        zip_code=request.POST.get('zip_code')
        street_name=request.POST.get('street_name')
        pickup_date_1=request.POST.get('pickup_date_1')
        pickup_date_2=request.POST.get('pickup_date_2')
        estimated_cost=request.POST.get('estimated_cost')
        product_list=request.POST.get('product_list')
        volumetric_weight=request.POST.get('volumetric_weight')
        estimated_weight=request.POST.get('estimated_weight')
        
        
        
       
    
        return render(request,"third_page.html",{"estimated_weight":estimated_weight,"volumetric_weight":volumetric_weight,"product_list":product_list,"pickup_date_1":pickup_date_1,"pickup_date_2":pickup_date_2,"estimated_cost":estimated_cost,"street_name":street_name,"house_number":house_number,"apartment_number":apartment_number,"town":town,"zip_code":zip_code,"delivery_type":delivery_type,"height":height,"weight":weight,"width":width,"recipient_name":recipient_name,"phone":phone,"country":country,"state":state,"length":length,
        })


