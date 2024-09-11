from django.urls import path
from api.views.view_app import *
from api.views.view_log import logs
from .views.view_auth import *
from .views import *


urlpatterns = [
    # logs
    path('logs/', logs.as_view(), name='logs'),
    # Authentication
    
    path('login/', login.as_view(), name='login'),
    path('register/', register_user.as_view(), name='register'),
    path('AllBranchesAndPermissions/', AllBranchesAndPermissions, name='AllBranchesAndPermissions'),
    

    path('ValidNumberOtpForRegisterView/', ValidNumberOtpForRegisterView.as_view(), name='ValidNumberOtpForRegisterView'),

    path('ValidNumberOtpView/', ValidNumberOtpView.as_view(), name='ValidNumberOtpView'),
    
    path('SendOtpView/', SendOtpView.as_view(), name='SendOtpView'),
    
    
    # populate_permissions
    path('nobody_should_use_this_api_please/', populate_permissions, name='populate_permissions'),
    
    # branches crud
    # path('branches/', BranchListCreateAPIView.as_view(), name='branch-list-create'),
    # path('branches/<int:pk>/', BranchDetailAPIView.as_view(), name='branch-detail'),
    path('branches/', BranchListCreateAPIView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', BranchDetailAPIView.as_view(), name='branch-detail'),
    
    path('branches/images/', BranchImageCreateAPIView.as_view(), name='branch-image-create'),
    path('branches/images/<int:pk>/', BranchImageDetailAPIView.as_view(), name='branch-image=details'),
    
    
    # URLs for Level
    path('levels/', LevelListCreateAPIView.as_view(), name='level-list-create'),
    path('levels/<int:pk>/', LevelDetailAPIView.as_view(), name='level-detail'),

    # URLs for Class
    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('classes/<int:pk>/', ClassDetailAPIView.as_view(), name='class-detail'),
    
    
    # URLs for stadiums
    path('stadiums/', StadiumListCreateAPIView.as_view(), name='stadium-list-create'),
    path('stadiums/<int:pk>/', StadiumDetailAPIView.as_view(), name='stadium-detail'),
]