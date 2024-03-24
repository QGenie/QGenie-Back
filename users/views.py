from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import parsers, renderers, status
from users.models import User, VerificationCode
from users.serializers import UserSerializer, UserCreationSerializer, ProfileSerializer, ProfilePictureSerializer, AuthTokenSerializer, UserResetPasswordSerializer
from users.custom_renderers import ImageRenderer
import jwt, datetime
import random


class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = jwt.encode({
                'email': serializer.validated_data['email'],
                'iat': datetime.datetime.now(datetime.timezone.utc),
                'nbf': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            }, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView): 
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        serializer2 = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) and serializer2.is_valid(raise_exception=True):
            instance = serializer.save()
            serializer2.save(user=instance)
        code = ''.join([str(random.choice(range(10))) for i in range(5)])
        verificationCode = VerificationCode(code=code, user=instance)
        verificationCode.save()
        data = serializer.validated_data
        data.update(serializer2.validated_data)
        print(data)
        subject = 'welcome to QGenie'
        message = f'Hi {data["first_name"]} {data["last_name"]} , thank you for registering in QGenie, your verification code is: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = (data['email'],)
        send_mail( subject, message, email_from, recipient_list )
        return Response({'email': data['email']})


class ResendVerificationCode(APIView): 
    def post(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        print(dir(user))
        if not user:
            return Response({'error': 'There is no user with such email'}, status=400)
        if user.profile.is_verified:
            return Response({'error': 'The Email is already verified'}, status=400)
        old_verification_code = VerificationCode.objects.filter(user=user)
        for code in old_verification_code:
            code.delete()
        code = ''.join([str(random.choice(range(10))) for i in range(5)])
        verificationCode = VerificationCode(code=code, user=user)
        verificationCode.save()
        subject = 'welcome to HomeCare'
        message = f'Hi {user.profile.first_name} {user.profile.last_name} , thank you for registering in HomeCare, your verification code is: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = (user.email,)
        send_mail( subject, message, email_from, recipient_list )
        return Response({'email': user.email})


class SignupVerificationView(APIView):  
    def post(self, request):
        code = request.data['code'] 
        user = User.objects.filter(email=request.data['email']).first()
        user_code = VerificationCode.objects.filter(user=user.id).first()   
        if code == user_code.code:
            user_code.delete()
            user.profile.is_verified = True
            user.save()
            return Response({'email': user.email})
        return Response({'error': 'Can\'t verify user'})


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_data = UserSerializer(instance=user).data
        profile_data = ProfileSerializer(instance=user.profile).data
        profile_data.pop('id')
        profile_data.pop('user')
        data = dict(**(user_data), **(profile_data))
        return Response(data=data)


class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    renderers_classes = [ImageRenderer]
    def post(self, request):
        profile = request.user.profile
        serializer = ProfilePictureSerializer(instance=profile, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=500)
    
    def get(self, request):
        data = User.objects.get(id=request.user.id).profile.picture
        return HttpResponse(data, content_type='image/' + data.path.split(".")[-1])

class ResetPasswordView(APIView): 
    def post(self, request):
        user = request.user
        opassword = request.data.get('opassword')
        if not user.check_password(opassword):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserResetPasswordSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response({'message': 'worked'})
