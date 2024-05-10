from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UserSerializer
from .models import User
import jwt, datetime
from django.utils import timezone
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        #Buscar usuário
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        #Validação de login
        if user is None:
            raise AuthenticationFailed('User not found!')
        elif not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        

        payload = {
            'id': user.id,
            'exp': timezone.now() + datetime.timedelta(minutes=60),
            'iat': timezone.now()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response  = Response({
            'jwt': token
        })
        
        return response