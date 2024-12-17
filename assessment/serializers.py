from rest_framework import serializers
from .models import Batch, ObjectRecord, ObjectData

class ObjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectData
        fields = ['key', 'value']

class ObjectRecordSerializer(serializers.ModelSerializer):
    data = ObjectDataSerializer(many=True)

    class Meta:
        model = ObjectRecord
        fields = ['object_id', 'data']

class BatchSerializer(serializers.ModelSerializer):
    objects = ObjectRecordSerializer(many=True)

    class Meta:
        model = Batch
        fields = ['batch_id', 'objects']

    def create(self, validated_data):
        # Extract the objects list
        objects_data = validated_data.pop('objects')
        
        # Create the Batch instance
        batch = Batch.objects.create(**validated_data)

        # Create the ObjectRecord and ObjectData instances
        for object_data in objects_data:
            object_record = ObjectRecord.objects.create(
                object_id=object_data['object_id'],
                batch=batch
            )
            for data in object_data['data']:
                ObjectData.objects.create(
                    object_record=object_record,
                    key=data['key'],
                    value=data['value']
                )

        return batch