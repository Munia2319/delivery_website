from rest_framework import serializers
from delivery.models import order_details

class order_Serializer(serializers.ModelSerializer):
    class Meta:
        model = order_details
        fields = ['recipient_name','phone']

