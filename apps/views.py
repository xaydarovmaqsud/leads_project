from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.core.mail import EmailMessage
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import Lead
from .serializers import LeadSerializer, LeadStatusUpdateSerializer
import mimetypes


class LeadCreateAPIView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        lead = serializer.save()

        send_mail(
            subject='Thank you for your submission!',
            message=f"Dear {lead.first_name},\n\nThank you for submitting your application. We’ll review it and contact you soon.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead.email],
            fail_silently=False,
        )

        reach_out_url = self.request.build_absolute_uri(
            reverse('lead-reach-out', args=[lead.id])
        )

        email = EmailMessage(
            subject='New Lead Submitted',
            body=f"A new lead has been submitted:\n\n"
                 f"Name: {lead.first_name} {lead.last_name}\n"
                 f"Email: {lead.email}\n\n"
                 f"Click the link below to mark as REACHED_OUT:\n{reach_out_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ATTORNEY_EMAIL],
        )

        if lead.resume:
            content_type, _ = mimetypes.guess_type(lead.resume.name)
            content_type = content_type or 'application/octet-stream'

            email.attach(
                lead.resume.name,
                lead.resume.read(),
                content_type
            )

        email.send(fail_silently=False)


class LeadListAPIView(generics.ListAPIView):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class LeadReachOutAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
            lead.status = 'REACHED_OUT'
            lead.save()
            return Response({"detail": "Lead status updated to REACHED_OUT."}, status=status.HTTP_200_OK)
        except Lead.DoesNotExist:
            return Response({"detail": "Lead not found."}, status=status.HTTP_404_NOT_FOUND)