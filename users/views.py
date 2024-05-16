from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import exceptions
from .serializer import UserSerializer
from .models import User, ForgetPassword
import jwt, datetime, random, string

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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response
    
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Usuário não autenticado')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuário não autenticado")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')

        response.data = {
            "Message": "Logout do usuário realizado"
        }
        return response
class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        
        ForgetPassword.objects.create(email=email, token=token)

        send_mail(
            subject='Reset your password',
            message='Click <a href="http://127.0.0.1:8000/api/forget">Here</a> for you reset your password'.format(token),
            from_email='martinsbarroskaua@gmail.com',
            recipient_list=[email]
        )      


        return Response({
            'message': 'sucesso!'
        })
    
class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        senha = data['password']

        if senha != data['password_confirm']:
            raise exceptions.APIException('As senhas não coincidem')
        
        passwordReset = ForgetPassword.objects.filter(token=data['token']).first()

        user = User.objects.filter(email=passwordReset.email).first()

        if not user:
            raise exceptions.NotFound("Usuário não encontrado!")
        
        user.set_password(senha)
        user.save()

        return Response({
            'message': "Senha recadastrada com sucesso!"
        })