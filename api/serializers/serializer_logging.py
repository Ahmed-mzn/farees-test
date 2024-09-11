from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from api.models import *

   
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'