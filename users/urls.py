from django.urls import path
from .views import PatientRegisterView

urlpatterns = [
    path('register', PatientRegisterView.as_view(), name="patient_register"),
]