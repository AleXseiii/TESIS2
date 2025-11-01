from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import PatientRegisterSerializer, PatientLoginSerializer
# Create your views here.

class PatientRegisterView(APIView):
    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                patient = serializer.save()
                token, _ = Token.objects.get_or_create(user=patient.user)

                return Response({
                    "status": True,
                    "message": "Paciente Registrado Correctamente",
                    "token": token.key,
                }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status":False,
            "errors":serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST)