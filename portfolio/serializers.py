from rest_framework import serializers
from .models import Customer,Investment

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('name', 'address', 'cust_number', 'city', 'state', 'zipcode', 'email', 'email', 'cell_phone')


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('customer','category','description','acquired_value','acquired_date','recent_value')