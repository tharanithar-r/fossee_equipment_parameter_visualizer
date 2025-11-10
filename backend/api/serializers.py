from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature')


class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'uploaded_at', 'total_count', 
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'min_flowrate', 'max_flowrate',
            'min_pressure', 'max_pressure',
            'min_temperature', 'max_temperature',
            'equipment', 'equipment_count'
        )
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class DatasetListSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'uploaded_at', 'total_count', 'equipment_count')
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()
