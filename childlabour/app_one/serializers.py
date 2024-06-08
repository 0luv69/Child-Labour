from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*




class CompSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'