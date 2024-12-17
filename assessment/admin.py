from django.contrib import admin
from .models import Batch, ObjectData, ObjectRecord

# Register your models here.
models = [Batch, ObjectData, ObjectRecord]
admin.site.register(models)
