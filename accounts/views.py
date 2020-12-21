from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Users, AmbulanceHub, Ambulance, Token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


class CreateUser(APIView):
    '''
    post datatype --> JSON
    required fields :- 
            username
            password
            email
            address (user home address)
    '''
    def post(self, request):
        if User.objects.filter(email=request.data['email']):
            return Response(data={'detail': 'This email is already registered'}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(username=request.data['username']):
            return Response(data={'detail': 'This username is already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'])
            user.is_active = False
            user.save()
            Users.objects.create(user=user, address=request.data['address'])
            token = Token.objects.create(user=user, purpose='user_activation').token
            domain = get_current_site(request).domain
            mail_subject = 'Activate your account'
            mail_body = 'Please click on the link below to activate your account.\n{}://{}/accounts/useractivation/{}'.format(request.scheme, domain, token)
            EmailMessage(mail_subject, mail_body, to=[request.data['email']]).send()
            return Response(data={'detail': 'User created successfully. After confirming your email you can login to your account.'}, status=status.HTTP_201_CREATED)


class UserActivation(APIView):
    def get(self, request, token):
        try:
            t = Token.objects.get(token=token)
            if t.purpose != 'user_activation':
                return Response(data={'detail': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = t.user
                user.is_active = True
                user.save()
                t.delete()
                return Response(data={'detail': 'User activated successfully'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'detail': 'Link is not valid'}, status=status.HTTP_404_NOT_FOUND)


# class CreateAmbulanceHub(APIView):
#     def post(self, request):
#         if User.objects.filter(email=request.data['email']):
#             return Response(data={'detail': 'This email is already registered'}, status=status.HTTP_400_BAD_REQUEST)
#         elif User.objects.filter(username=request.data['username']):
#             return Response(data={'detail': 'This username is already registered'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'])
#             user.is_active = False
#             user.save()
#             AmbulanceHub.objects.create(user=user, name=request.data['name'], address=request.data['address'], location=request.data['location'])
#             return Response(data={'detail': 'Ambulance Hub created successfully'}, status=status.HTTP_201_CREATED)
