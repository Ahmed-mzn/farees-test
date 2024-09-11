from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from api.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# serializers



class AllBranchesAndPermissionsSerializer(serializers.ModelSerializer):
    all_permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'all_permissions']
    def get_all_permissions(self, obj):
        branch_permissions = []
        categories = PermissionCategory.objects.all()
        for categorie in categories:
            branch_permissions_names = []
            categorie_permissions_names = PermissionName.objects.filter(category=categorie)
            for categorie_permissions_name in categorie_permissions_names:
                branch_permissions_names.append({"name": categorie_permissions_name.name})

            branch_permissions.append({
                'categorie_id': categorie.id,
                'categorie_name': categorie.name,
                'sub_permissions': branch_permissions_names
            })

        return branch_permissions
        
        
class PermissionSerializer(serializers.ModelSerializer):
 
    permission_name = serializers.CharField(source='permission.name')
    category_name = serializers.CharField(source='permission.category.name')

    class Meta:
        model = UserPermissionAssign
        fields = ['id','permission_name', 'category_name']

class BranchPermissionSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(source='branch_permissions', many=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'permissions']

class UserSerializer(serializers.ModelSerializer):
    branches = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = NewUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'telephone', 'profile_picture','branches']
    def get_branches(self, obj):
        user_permissions = UserPermissionAssign.objects.filter(user=obj).values('branch').distinct()
        
        branch_permissions = []
        
        # Iterate through each unique branch the user has access to
        for branch_data in user_permissions:
            branch = Branch.objects.get(id=branch_data['branch'])  # Get the branch by its ID
            
            # Get all permissions for this user and this branch
            permissions = UserPermissionAssign.objects.filter(user=obj, branch=branch)
            
            branch_permissions.append({
                'branch_id': branch.id,
                'branch_name': branch.name,
                'permissions': PermissionSerializer(permissions, many=True).data
            })

        return branch_permissions

    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return ""
    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        userserializer = UserSerializer(user, many=False)
        login_infos = userserializer.data
        login_infos['token']=token['access']
        login_infos['refresh']=token['refresh']
        return login_infos