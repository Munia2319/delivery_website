from django.db import models


# Create your models here.
class delivery_rate(models.Model):
    country=models.CharField(max_length=50)
    weight=models.FloatField()
    amount=models.FloatField()
    delivery_type=models.CharField(max_length=50)

    def __str__(self):
        return self.country

class products(models.Model):
    product_name=models.CharField(max_length=200)
    product_type=models.IntegerField()

    def __str__(self):
        return self.product_name


class additional_charges(models.Model):
    scheme_name=models.CharField(max_length=100)
    scheme_type=models.IntegerField()
    charge_per_transaction=models.FloatField()

    
    def __str__(self):
        return self.scheme_name

    


class order_details(models.Model):
    recipient_name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    town=models.CharField(max_length=200)
    house_number=models.CharField(max_length=200)
    street_name=models.CharField(max_length=200)
    apartment_number=models.CharField(max_length=200)
    zip_code=models.CharField(max_length=200)
    product_details=models.CharField(max_length=1000)
    delivery_type=models.CharField(max_length=200)
    pickup_date_start=models.CharField(max_length=200)
    pickup_date_end=models.CharField(max_length=200)
    delivery_status=models.CharField(max_length=200)
    estimated_weight=models.FloatField()
    estimated_cost=models.FloatField()
    volumetric_weight=models.FloatField()

    def __str__(self):
         return self.recipient_name

class currency_rate(models.Model):
    currency_code=models.CharField(max_length=200)
    rate=models.FloatField()
   
    def __str__(self):
         return self.currency_code
    