from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Batch, ObjectRecord, ObjectData
from .serializers import BatchSerializer, ObjectRecordSerializer

class SubmitBatchView(APIView):
   def post(self, request):
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            # Save the batch and its nested objects (ObjectRecord, ObjectData) via the serializer
            with transaction.atomic():
                batch = serializer.save()  # This will call the custom create() method
            return Response({'message': 'Batch submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveObjectView(APIView):
    def get(self, request, object_id):
        try:
            object_record = ObjectRecord.objects.prefetch_related('data').get(object_id=object_id)
            serializer = ObjectRecordSerializer(object_record)
            return Response(serializer.data)
        except ObjectRecord.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

class FilterObjectsView(APIView):
    def get(self, request):
        key = request.query_params.get('key')
        value = request.query_params.get('value')
        filters = {}
        if key:
            filters['data__key'] = key
        if value:
            filters['data__value'] = value

        object_records = ObjectRecord.objects.prefetch_related('data').filter(**filters).distinct()
        serializer = ObjectRecordSerializer(object_records, many=True)
        return Response(serializer.data)
