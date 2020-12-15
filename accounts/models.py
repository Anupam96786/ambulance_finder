from django.db import models
from django.contrib.auth.models import User


# class User_type_connection(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', unique=True, blank=False, null=False)
#     user_type = 


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    address = models.CharField('Address', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Ambulance_hub(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    address = models.CharField('Address', max_length=100, blank=True, null=True)
    location = models.CharField('Location', max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Ambulance Hub'
        verbose_name_plural = 'Ambulance Hubs'


class Ambulance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    ambulance_no = models.CharField('Ambulance Number', max_length=30, unique=True)
    hub = models.ForeignKey(Ambulance_hub, on_delete=models.CASCADE)
    available = models.BooleanField('Available')
