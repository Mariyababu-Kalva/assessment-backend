from django.db import models

class Batch(models.Model):
    batch_id = models.CharField(max_length=255, unique=True)

class ObjectRecord(models.Model):
    object_id = models.CharField(max_length=255, unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='objects')

class ObjectData(models.Model):
    object_record = models.ForeignKey(ObjectRecord, on_delete=models.CASCADE, related_name='data')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)