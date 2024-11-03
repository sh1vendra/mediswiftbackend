from rest_framework import serializers
from . import models

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Query
        fields = '__all__'
    
class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Treatment
        fields = '__all__'