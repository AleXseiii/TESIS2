from django.urls import path
from .views import DoctorListView

urlpatterns = [
    path('doctors', DoctorListView.as_view(), name='doctor-list'),
]
