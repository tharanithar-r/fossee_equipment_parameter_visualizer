from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.http import FileResponse
from django.db.models import Count
import pandas as pd
import os
from .models import Dataset, Equipment
from .serializers import UserSerializer, DatasetSerializer, DatasetListSerializer, EquipmentSerializer
from .utils import generate_pdf_report


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetSerializer
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read CSV
            df = pd.read_csv(file)
            
            # Validate columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Clean data
            df = df.dropna()
            
            # Calculate statistics
            stats = {
                'total_count': len(df),
                'avg_flowrate': float(df['Flowrate'].mean()),
                'avg_pressure': float(df['Pressure'].mean()),
                'avg_temperature': float(df['Temperature'].mean()),
                'min_flowrate': float(df['Flowrate'].min()),
                'max_flowrate': float(df['Flowrate'].max()),
                'min_pressure': float(df['Pressure'].min()),
                'max_pressure': float(df['Pressure'].max()),
                'min_temperature': float(df['Temperature'].min()),
                'max_temperature': float(df['Temperature'].max()),
            }
            
            # Save file
            upload_dir = 'media/uploads'
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.name)
            
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Create dataset
            dataset = Dataset.objects.create(
                user=request.user,
                name=file.name,
                file_path=file_path,
                **stats
            )
            
            # Create equipment records
            equipment_list = []
            for _, row in df.iterrows():
                equipment_list.append(Equipment(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                ))
            Equipment.objects.bulk_create(equipment_list)
            
            # Keep only last 5 datasets
            user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
            if user_datasets.count() > 5:
                old_datasets = user_datasets[5:]
                for old_dataset in old_datasets:
                    if os.path.exists(old_dataset.file_path):
                        os.remove(old_dataset.file_path)
                    old_dataset.delete()
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        dataset = self.get_object()
        
        # Get type distribution
        type_distribution = list(
            dataset.equipment.values('equipment_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        return Response({
            'id': dataset.id,
            'name': dataset.name,
            'uploaded_at': dataset.uploaded_at,
            'total_count': dataset.total_count,
            'statistics': {
                'flowrate': {
                    'avg': dataset.avg_flowrate,
                    'min': dataset.min_flowrate,
                    'max': dataset.max_flowrate
                },
                'pressure': {
                    'avg': dataset.avg_pressure,
                    'min': dataset.min_pressure,
                    'max': dataset.max_pressure
                },
                'temperature': {
                    'avg': dataset.avg_temperature,
                    'min': dataset.min_temperature,
                    'max': dataset.max_temperature
                }
            },
            'type_distribution': type_distribution
        })
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        dataset = self.get_object()
        
        try:
            pdf_path = generate_pdf_report(dataset)
            response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
