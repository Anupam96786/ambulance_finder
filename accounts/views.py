from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users, AmbulanceHub, Ambulance, Token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from rest_framework import permissions
from django.contrib.gis.geos import Point


class AllowSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return all(request.user.is_admin, request.user.is_staff)


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
                return Response(data={'detail': 'User activated successfully. Now you can login to your account.'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'detail': 'Link is not valid'}, status=status.HTTP_404_NOT_FOUND)


class CreateAmbulanceHub(APIView):
    '''
    post datatype --> JSON
    required fields :- 
            username
            password
            email
            address (user home address(char type field))
            name (Ambulance Hub name)
            lat
            long
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
            AmbulanceHub.objects.create(user=user, name=request.data['name'], address=request.data['address'], location=Point(request.data['long'], request.data['lat'], srid=4326))
            token = Token.objects.create(user=user, purpose='hub_activation').token
            domain = get_current_site(request).domain
            mail_subject = 'Ambulance hub request'
            mail_body = 'Hi Admin,\n\n{} has applied to open an Ambulance Hub. After verifying all of the details click on the link below to activate that hub.\n{}://{}/accounts/hubactivation/{}'.format(request.data['username'],request.scheme, domain, token)
            admin_mail = list(list(zip(*list(User.objects.filter(is_superuser=True, is_staff=True).values_list('email'))))[0])
            EmailMessage(mail_subject, mail_body, to=admin_mail).send()
            mail_subject = 'Registration successful'
            mail_body = 'Hi {},\nWe have received your request. We will verify your deatils and activate your account. You will get another email when your request will be accepted.'.format(request.data['username'])
            EmailMessage(mail_subject, mail_body, to=[request.data['email']]).send()
            return Response(data={'detail': 'Ambulance Hub created successfully. After confirmation from admins you can login to your account.'}, status=status.HTTP_201_CREATED)


class AmbulanceHubActivation(APIView):
    permission_classes = (AllowSuperuser,)
    def get(self, request, token):
        try:
            t = Token.objects.get(token=token)
            if t.purpose != 'hub_activation':
                return Response(data={'detail': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = t.user
                user.is_active = True
                user.save()
                t.delete()
                to_mail = user.email
                mail_subject = 'Your Hub Activated'
                mail_body = 'Your request for hub creation was accepted. Now you can login to your hub account.'
                EmailMessage(mail_subject, mail_body, to=[to_mail]).send()
                return Response(data={'detail': 'Hub activated successfully'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'detail': 'Link is not valid'}, status=status.HTTP_404_NOT_FOUND)


# class CreateAmbulance(APIView):

