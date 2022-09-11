from ast import Delete, Expression
import email
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from customUser.utils import Util
from .serializers import ChangePasswordSerializer, UserSerializer
from customUser.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
# from django_email_verification import verify_view, verify_token, send_email
import jwt
from django.conf import settings
from django.template.response import TemplateResponse
from rest_framework.permissions import IsAuthenticated


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getUser(request, pk):
    queryset = CustomUser.objects.get(id=pk)
    serializer = UserSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def userCreate(request):

    serializer = UserSerializer(data=request.data)

    print(request.data)
    if serializer.is_valid():
        serializer.save()

        user = CustomUser.objects.get(email=request.data['email'])
        user.save()
        current_site = get_current_site(request).domain

        relativeLink = reverse('verify-email')

        token = RefreshToken.for_user(user).access_token
        absurl = "http://"+current_site + \
            relativeLink+"?token=" + str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'verify_url': absurl,
                'email_subject': 'Verify your email', 'email_body': email_body, 'to_email': user.email, 'user': user}

        Util.send_email(data)

        # user.is_active = False  # Example
        # send_email(user)
        return Response("success")
    else:
        print(serializer.errors)
        return Response(serializer.errors)

# @verify_view
# def confirm(request, token):
#     success, user = verify_token(token)
#     return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')


@api_view(['POST'])
@permission_classes([AllowAny])
def resendEmailVerifcation(request):
    user = CustomUser.objects.get(email=request.data['email'])

    current_site = get_current_site(request).domain

    relativeLink = reverse('verify-email')

    token = RefreshToken.for_user(user).access_token
    absurl = "http://"+current_site + \
        relativeLink+"?token=" + str(token)
    email_body = 'Hi '+user.username + \
        ' Use the link below to verify your email \n' + absurl
    data = {'verify_url': absurl,
            'email_subject': 'Verify your email', 'email_body': email_body, 'to_email': user.email, 'user': user}

    Util.send_email(data)
    return Response("sent")


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        print(jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']))
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

                return TemplateResponse(request, 'email_success.html', {}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as id:
            return Response({"error": "Link Expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as id:
            return Response({"error": "Invalid Link"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def userUpdate(request, pk):
    user = CustomUser.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    print(serializer.data)
    return Response(serializer.data)


@api_view(['DELETE'])
def userDelete(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.delete()
    return Response('Deleted')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
