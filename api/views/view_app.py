from rest_framework import generics
from api.models import *
from api.serializers.serializer_app import *

class BranchListCreateAPIView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class BranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class BranchImageCreateAPIView(generics.CreateAPIView):
    queryset = Branch_image.objects.all()
    serializer_class = BranchImageCreateSerializer

class BranchImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch_image.objects.all()
    serializer_class = BranchImageCreateSerializer
    
    
class LevelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class LevelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    
    
class ClassListCreateAPIView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    
class StadiumListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer

class StadiumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer