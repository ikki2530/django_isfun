from django.urls import path
from .views import fallBackAPIView

urlpatterns = [
    path('api/v1/fallback/', fallBackAPIView.as_view()),
]