from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Batch, ObjectRecord, ObjectData

class SubmitBatchViewTests(TestCase):
    def test_submit_batch_success(self):
        url = reverse('submit-batch')
        payload = {
            "batch_id": "batch_001",
            "objects": [
                {
                    "object_id": "object_001",
                    "data": [
                        {"key": "color", "value": "blue"},
                        {"key": "size", "value": "large"}
                    ]
                },
                {
                    "object_id": "object_002",
                    "data": [
                        {"key": "shape", "value": "circle"}
                    ]
                }
            ]
        }

        response = self.client.post(url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "Batch submitted successfully"})
        self.assertTrue(Batch.objects.filter(batch_id="batch_001").exists())
        self.assertTrue(ObjectRecord.objects.filter(object_id="object_001").exists())
        self.assertTrue(ObjectData.objects.filter(key="color", value="blue").exists())

    def test_submit_batch_invalid_payload(self):
        url = reverse('submit-batch')
        payload = {
            "batch_id": "batch_001",
            # Missing objects
        }

        response = self.client.post(url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("objects", response.json())

class RetrieveObjectViewTests(TestCase):
    def test_retrieve_object_success(self):
        batch = Batch.objects.create(batch_id="batch_001")
        object_record = ObjectRecord.objects.create(object_id="object_001", batch=batch)
        ObjectData.objects.create(object_record=object_record, key="color", value="blue")

        url = reverse('retrieve-object', kwargs={"object_id": "object_001"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["object_id"], "object_001")
        self.assertTrue(any(data["key"] == "color" and data["value"] == "blue" for data in response.json()["data"]))

    def test_retrieve_object_not_found(self):
        url = reverse('retrieve-object', kwargs={"object_id": "nonexistent_object"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "Object not found"})

class FilterObjectsViewTests(TestCase):
    def test_filter_objects_by_key(self):
        batch = Batch.objects.create(batch_id="batch_001")
        object_record = ObjectRecord.objects.create(object_id="object_001", batch=batch)
        ObjectData.objects.create(object_record=object_record, key="color", value="blue")

        url = reverse('filter-objects')
        response = self.client.get(url, {"key": "color"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["object_id"], "object_001")

    def test_filter_objects_by_key_and_value(self):
        batch = Batch.objects.create(batch_id="batch_001")
        object_record = ObjectRecord.objects.create(object_id="object_001", batch=batch)
        ObjectData.objects.create(object_record=object_record, key="color", value="blue")

        url = reverse('filter-objects')
        response = self.client.get(url, {"key": "color", "value": "blue"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["object_id"], "object_001")

    def test_filter_objects_no_results(self):
        batch = Batch.objects.create(batch_id="batch_001")
        object_record = ObjectRecord.objects.create(object_id="object_001", batch=batch)
        ObjectData.objects.create(object_record=object_record, key="color", value="blue")

        url = reverse('filter-objects')
        response = self.client.get(url, {"key": "nonexistent_key"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
