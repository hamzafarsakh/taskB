from rest_framework import serializers

from .models import *

# serializers.py



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Active
        fields = '__all__'
