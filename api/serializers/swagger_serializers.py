from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from api.models import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

AR = 'AR'
FR = 'FR'
EN = 'EN'

LANGUAGE_CHOICES = (
    (AR, 'AR'),
    (FR, 'FR'),
    (EN, 'EN'),
)
class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    telephone = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    password = serializers.CharField()
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    
    profile_picture = serializers.CharField()
    identity = serializers.CharField()
    permis = serializers.CharField()
    device_id = serializers.CharField()
        

    
class UserInfoSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    email = serializers.CharField()
    telephone = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    password = serializers.CharField()
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    profile_picture = serializers.CharField()
    status = serializers.CharField()
    identity = serializers.CharField()
    permis = serializers.CharField()

class UserLoginBodySerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    
class JsonFormatInvalidSerializer(serializers.Serializer):
    msg = serializers.CharField()
    class Meta:
        swagger_schema_fields = {
            'msg': openapi.Schema(
                title="Json format invalid",
                type=openapi.TYPE_STRING,
                description="It appers when the user sent bad formatted json keys and values"
            )
        }
    
    
   

class CheckUserExistenceSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()
    telephone = serializers.CharField()

class Sendotp(serializers.Serializer):
    telephone = serializers.IntegerField()
    
    
class ValidNumberOtpSerializer(serializers.Serializer):
    telephone = serializers.IntegerField()
    otp = serializers.CharField()  
    
class SuccesSerializer(serializers.Serializer):
    msg = serializers.CharField()  
    class Meta:
        swagger_schema_fields = {
            'msg': openapi.Schema(
                title="A message of succes depends on the given informations",
                type=openapi.TYPE_STRING,
                description="It appers when the action done succesfully always with 200 as a response code"
            )
        } 
    
class FailedSerializer(serializers.Serializer):
    msg = serializers.CharField()
    class Meta:
        swagger_schema_fields = {
            'msg': openapi.Schema(
                title="A message of failing depends on the given informations",
                type=openapi.TYPE_STRING,
                description="It appers when the action done with failure always with 400 as a response code"
            )
        } 
    
class UnauthorizedSerializer(serializers.Serializer):
    detail = serializers.CharField()
    class Meta:
        swagger_schema_fields = {
            'detail': openapi.Schema(
                title="Unauthorized",
                type=openapi.TYPE_STRING,
                description="Authentication credentials were not provided."
            )
        } 
        
class AvailableCarsBodySerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    min_price=models.CharField()
    max_price=models.CharField()
    category_id=models.CharField()