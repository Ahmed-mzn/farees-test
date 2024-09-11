from rest_framework import serializers
from api.models import *



class BranchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch_image
        fields = ['id', 'picture']
        
class BranchSerializer(serializers.ModelSerializer):
    branche_image = BranchImageSerializer(many=True, read_only=True)
    class Meta:
        model = Branch
        fields = ['id', 'name', 'description', 'location', 'telephone', 'partner_name', 'partner_percentage', 'branche_image']
  
  
class BranchImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch_image
        fields = ['branch', 'picture']      
        
        
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
        
class ClassSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(slug_field='name', queryset=Level.objects.all())

    class Meta:
        model = Class
        fields = ['id', 'name', 'level', 'age_from', 'age_to']
        
        
class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['id', 'name', 'size', 'location', 'photos', 'branch']