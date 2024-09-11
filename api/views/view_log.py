from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers.serializer_logging import LogSerializer
from drf_spectacular.utils import extend_schema
from django.db.models import Q
from api.serializers.swagger_serializers import JsonFormatInvalidSerializer




class logs(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary='Logs api',
        description='Logs api returns last 100 call you make',
        tags=['Logs api'],
        responses={
            200: LogSerializer(many=True),
            401: JsonFormatInvalidSerializer
        }
    )
    def get(self,request):
        included_paths = [
            '/api/logs/', 
            '/api/login/', 
            '/api/register/', 
            '/api/AllBranchesAndPermissions/', 
            '/api/ValidNumberOtpForRegisterView/', 
            '/api/ValidNumberOtpView/', 
            '/api/SendOtpView/', 
            '/api/nobody_should_use_this_api_please/', 
            '/api/branches/', 
            '/api/branches/<int:pk>/', 
            '/api/branches/images/', 
            '/api/branches/images/<int:pk>/', 
            '/api/levels/', 
            '/api/levels/<int:pk>/', 
            '/api/classes/', 
            '/api/classes/<int:pk>/',
            '/api/stadiums/', 
            '/api/stadiums/<int:pk>/' 
        ]

        
        logs_to_keep = APILog.objects.filter(query).order_by('-request_date')[:100].values_list('id', flat=True)
        APILog.objects.exclude(id__in=logs_to_keep).delete()
        
        query = Q()
        for path in included_paths:
            query |= Q(path__startswith=path)

        logs = APILog.objects.filter(query).order_by('-request_date')[:100]
        data = LogSerializer(logs, many=True).data
        return Response(data)
    # /api/docs/schema