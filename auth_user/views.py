from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({
                "status": False,
                "message": "Email y password son requeridos"
            }, status=status.HTTP_400_BAD_REQUEST)

    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "Credenciales inválidas"
            }, status=status.HTTP_401_UNAUTHORIZED)

    
        user = authenticate(username=user.username, password=password)

        if not user:
            return Response({
                "status": False,
                "message": "Credenciales inválidas"
            }, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        profile = None
        if user.is_superuser:
            role = "superadmin"
        elif hasattr(user, "kinesiologist"):
            profile =  user.kinesiologist
            role = "kinesiologist"
        elif hasattr(user, "patient"):
            profile =  user.patient
            role = "patient"
        else:
            role = "unknown"

        if profile != None:
            if role == "kinesiologist":
                return Response({
                            "status": True,
                            "token": token.key,
                            "email":user.email,
                            "role":role,
                            "user": {
                                "id": profile.id,
                                "name": profile.name,
                                "rut": profile.rut,
                                "specialty": profile.specialty,
                                "email": user.email,
                                "phone_number": profile.phone_number,
                                "box": profile.box,
                                "image_url": profile.image_url
                            }
                        })
            elif role == "patient":
                return Response({
                            "status": True,
                            "token": token.key,
                            "email":user.email,
                            "role":role,
                            "user": {
                                "id": profile.id,
                                "name": profile.name,
                                "rut": profile.rut,
                                "email": user.email,
                                "phone_number": profile.phone_number,
                                "diagnostic": profile.diagnostic

                            }
                        })
        else:
            return Response({
                "status": True,
                "token": token.key,
                "email":user.email,
                "role":role
            })  