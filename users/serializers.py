from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient

class PatientRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Patient
        fields = ['name','rut','email','password','diagnostic','phone_number']

    def validate(self, data):    
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError({"email": "Este email ya está registrado"})

            return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        name = validated_data['name']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        patient = Patient.objects.create(
            user=user,
            **validated_data
        )

        return patient
    
    
    

class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()