from django.contrib import admin
from .models import Dataset, Equipment


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'uploaded_at', 'total_count')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset')
    list_filter = ('equipment_type', 'dataset')
    search_fields = ('equipment_name', 'equipment_type')
