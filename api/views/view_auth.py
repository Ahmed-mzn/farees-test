import json
from django.http import JsonResponse
from rest_framework.authentication import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.serializer_auth import *
from api.models import *
from django.core.files import File
import os
from datetime import date, timedelta
from django.db import IntegrityError
from environs import Env
from api.serializers.swagger_serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from api.models import PermissionName, PermissionCategory, UserPermissionAssign
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json

from api.utils import sms_sender
env = Env()
env.read_env()

    
@api_view(['GET'])
def AllBranchesAndPermissions(request):
    branches = Branch.objects.all()
    serializer = AllBranchesAndPermissionsSerializer(branches, many=True)
    return Response(serializer.data)
            

#used
class login(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary='User login',
        description='login api',
        tags=['Login'],
        request= UserLoginBodySerializer,
        responses={
            200: UserSerializer,
            400: FailedSerializer,
            404: JsonFormatInvalidSerializer
        }
    )
    def post(self, request):
        try:
            body = json.loads(request.body)
            email = body.get('email')
            password = body.get('password')
            
            
            user = NewUser.objects.filter(email=email).first()
            
            res = user.check_password(password)
            if not res:
                return JsonResponse({'msg': f'invalid email or password'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'msg': 'json format invalid'}, status=404)
        
        if user is not None:
                userserializer = UserSerializer(user, many=False)
                refresh = RefreshToken.for_user(user)
                login_infos = userserializer.data
                login_infos['access'] = str(refresh.access_token)
                login_infos['refresh'] = str(refresh)
                return JsonResponse(
                    login_infos
                    )
            
        return JsonResponse({'msg': f'invalid email or password'}, status=400)


class register_user(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
    summary='User Registration',
    description='API for user registration',
    tags=['Login'],
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: FailedSerializer,
        404: JsonFormatInvalidSerializer
    }
)
    def post(self, request):

        # NewUser.objects.all().delete()
        # UserPermissionAssign.objects.all().delete()
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            
            roles_list = ['ADMIN','COACH','PARENT']

            email = data.get('email')
            username = data.get('username')
            role = data.get('role')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            telephone = data.get('telephone')
            password = data.get('password', '123456789')

            if role not in roles_list:
                return JsonResponse(
                    {"msg":"the role choices must be ADMIN, COACH or PARENT"}, status=400
                )
            if role =="PARENT":
                result = sms_sender(telephone, "أهلا بــكم ولي الأمر في أكاديمية فارس, رمز تحققكم هو : ", 2057)
                if result is None:
                    return JsonResponse(
                    {"msg":"Failed to send the otp"}, status=400
                    )
            
            # Create the user
            user = NewUser.objects.create_user(
                email=email,
                username=username,
                role=role,
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                password=password
            )
            if role=="PARENT":
                return JsonResponse(
                    {"msg":"The user has been created, the otp has been sent."}, status=200
                    )
            # Handle branches and permissions
            branches_permissions = data.get('branches_permissions', [])
            
            # Loop through each branch and assign the relevant permissions
            for branch_data in branches_permissions:
                branch_id = branch_data.get('branch_id')
                permissions = branch_data.get('permissions', {})

                try:
                    # Fetch the branch
                    branch = Branch.objects.get(id=branch_id)

                    # Loop through each category and assign permissions
                    for category_name, permission_list in permissions.items():
                        try:
                            category = PermissionCategory.objects.get(name=category_name)
                            assign_permissions_to_user(user, permission_list, category, branch)
                        except PermissionCategory.DoesNotExist:
                            continue  # Skip the category if it doesn't exist
                except Branch.DoesNotExist:
                    continue  # Skip if the branch doesn't exist
            userserializer = UserSerializer(user, many=False)
            refresh = RefreshToken.for_user(user)
            login_infos = userserializer.data
            login_infos['access'] = str(refresh.access_token)
            login_infos['refresh'] = str(refresh)
            return JsonResponse(
                login_infos, status=201
                )

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def assign_permissions_to_user(user, permission_list, category, branch):
    print(user, permission_list, category, branch)
    for permission_name in permission_list:
        try:
            permission = PermissionName.objects.get(category=category, name=permission_name)
            UserPermissionAssign.objects.create(user=user, permission=permission, branch=branch)
        except PermissionName.DoesNotExist:
            continue  # Skip if the permission doesn't exist
        
        
        

class ValidNumberOtpForRegisterView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary='Valid number',
        description='Valid number',
        tags=['Login'],
        request= ValidNumberOtpSerializer,
        responses={
            200: UserSerializer,
            400: FailedSerializer,
            404: JsonFormatInvalidSerializer
        }
    )
    def post(self, request):
        try:
            data_request = json.loads(request.body.decode('utf-8'))
            try:
                phone = data_request['telephone']
                otp = data_request['otp']
            except:
                return JsonResponse({'msg': 'json format invalid'}, status=404)
            ten_minutes_ago = timezone.now() - timedelta(days=10)
            o = OtpMail.objects.filter(telephone=phone, otp=otp, created_at__gte=ten_minutes_ago).last()
            if o is not None:
                o.validated = True
                o.save()
                user= NewUser.objects.get(telephone=phone)
                user.is_active=True
                userserializer = UserSerializer(user, many=False)
                refresh = RefreshToken.for_user(user)
                login_infos = userserializer.data
                login_infos['access'] = str(refresh.access_token)
                login_infos['refresh'] = str(refresh)
                return JsonResponse(
                    login_infos, status=201
                    )
            
            return Response({"msg": "Invalid informations"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)      
        

class SendOtpView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary='Send otp',
        description='Send OTP',
        tags=['Login'],
        request= Sendotp,
        responses={
            200: SuccesSerializer,
            400: FailedSerializer,
            401: FailedSerializer,
            404: JsonFormatInvalidSerializer
        }
    )
    def post(self, request):
            
        data_request = json.loads(request.body.decode('utf-8'))
        try:
            phone = data_request['telephone']
            user= NewUser.objects.get(telephone=phone)
        except NewUser.DoesNotExist:
            return JsonResponse({'msg': 'Unable to find a user with this informations'}, status=401)
        except:
            return JsonResponse({'msg': 'json format invalid'}, status=404)
        if user.role not in ['PARENT', 'COACH']:
            return JsonResponse({'msg': 'This endpoint api is only for parents or coachs'}, status=404)
        result = sms_sender(phone, "أهلا بــكم في أكاديمية فارس, رمز تحققكم هو : ", 2107)
        if result is None:
            return JsonResponse(
            {"msg":"Failed to send the otp"}, status=400
            )
        else:
            return JsonResponse(
                    {"msg":"the otp has been sent."}, status=200
                    )


class ValidNumberOtpView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary='Valid otp',
        description='Valid otp',
        tags=['Login'],
        request= ValidNumberOtpSerializer,
        responses={
            200: UserSerializer,
            400: FailedSerializer,
            404: JsonFormatInvalidSerializer
        }
    )
    def post(self, request):
        try:
            data_request = json.loads(request.body.decode('utf-8'))
            try:
                phone = data_request['telephone']
                otp = data_request['otp']
            except:
                return JsonResponse({'msg': 'json format invalid'}, status=404)
            ten_minutes_ago = timezone.now() - timedelta(days=10)
            print(phone, otp, ten_minutes_ago)
            o = OtpMail.objects.filter(telephone=phone, otp=otp, created_at__gte=ten_minutes_ago).last()
            print(o)
            print("***")
            if o is not None:
                user= NewUser.objects.get(telephone=phone)
                userserializer = UserSerializer(user, many=False)
                refresh = RefreshToken.for_user(user)
                login_infos = userserializer.data
                login_infos['access'] = str(refresh.access_token)
                login_infos['refresh'] = str(refresh)
                return JsonResponse(
                    login_infos, status=201
                    )
            
            return Response({"msg": "Invalid informations"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)                 
                   
# creating permissions to database
@api_view(['GET'])
def populate_permissions(request):
    categories = {
        "branch": ["can_see", "can_edit", "can_delete", "can_freeze"],
        "level": ["can_see", "can_edit", "can_delete", "can_freeze", "can_hide"],
        "class": ["can_see", "can_edit", "can_delete", "can_freeze", "can_hide"],
        "timing_periods": ["can_see", "can_edit", "can_delete", "can_freeze", "can_hide", "can_stop_subscription"],
        "coach": ["can_see", "can_edit", "can_delete"],
        "training_sessions": ["can_see", "can_edit", "can_delete", "can_freeze", "can_hide", "can_take_presence", "can_stop_subscription", "merge_training_sessions"],
        "subscribers": ["can_see", "can_edit", "can_delete", "move_subscriber", "can_freeze"],
        "reports": ["can_see_global_report", "can_see_sessions_report", "can_see_subscribers_report"]
    }
    NewUser.objects.all().delete()
    PermissionCategory.objects.all().delete()
    PermissionName.objects.all().delete()
    Branch.objects.all().delete()
    for category_name, permissions in categories.items():
        category, created = PermissionCategory.objects.get_or_create(name=category_name)
        for permission_name in permissions:
            PermissionName.objects.get_or_create(category=category, name=permission_name)
            
    b = Branch.objects.create(name="Mekkah", description="Central Branch", location="maps.google.com/54d545655s", telephone=5825885)    
    b = Branch.objects.create(name="El-Medinah", description="Best Branch", location="maps.google.com/54d545655s", telephone=5825886)
    return JsonResponse({'msg': "done"}, safe=False, status=200)