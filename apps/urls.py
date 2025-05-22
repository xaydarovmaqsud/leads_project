from django.urls import path
from .views import LeadCreateAPIView, LeadListAPIView, LeadStatusUpdateAPIView, LeadReachOutAPIView

urlpatterns = [
    path('leads/', LeadCreateAPIView.as_view(), name='lead-create'),
    path('leads/<uuid:pk>/reach-out/', LeadReachOutAPIView.as_view(), name='lead-reach-out'),
    path('internal/leads/', LeadListAPIView.as_view(), name='lead-list'),
    path('internal/leads/<uuid:id>/status/', LeadStatusUpdateAPIView.as_view(), name='lead-status-update'),
]
