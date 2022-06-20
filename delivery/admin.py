from django.contrib import admin
from delivery.models import delivery_rate,products,additional_charges,order_details,currency_rate

# Register your models here.
class delivery_rateAdmin(admin.ModelAdmin):
    list_filter=('country',)
admin.site.register(delivery_rate, delivery_rateAdmin)

admin.site.register(products)
admin.site.register(additional_charges)
admin.site.register(order_details)
admin.site.register(currency_rate)



