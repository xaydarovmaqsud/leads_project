from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Lead


class LeadAPITestCase(APITestCase):
    def setUp(self):
        self.resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        self.create_url = reverse('lead-create')
        self.lead_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "resume": self.resume
        }

    def test_create_lead(self):
        response = self.client.post(self.create_url, self.lead_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.first().email, "john@example.com")

    def test_lead_list_unauthenticated(self):
        list_url = reverse('lead-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reach_out_link(self):
        lead = Lead.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            resume=self.resume
        )
        url = reverse('lead-reach-out', args=[str(lead.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lead.refresh_from_db()
        self.assertEqual(lead.status, 'REACHED_OUT')
