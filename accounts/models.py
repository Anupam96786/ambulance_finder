from django.db import models
from django.contrib.auth.models import User


class AccountType(models.Model):
    account_type = [
        ('user', 'User'),
        ('ambulance_hub', 'Ambulance Hub'),
        ('ambulance', 'Ambulance'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User', blank=False, null=False, primary_key=True)
    type = models.CharField(verbose_name='Account Type', choices=account_type, default='user', blank=False, null=False, max_length=20)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    address = models.CharField('Address', max_length=100, blank=True, null=True)    # user home address

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        AccountType.objects.create(user=self.user, type='user')
        super(Users, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username


class AmbulanceHub(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    name = models.CharField(verbose_name='Hub Name', max_length=30, blank=False, null=False)    # Ambulance hub name to be displayed in user panel
    address = models.CharField('Address', max_length=100, blank=True, null=True)
    location = models.CharField('Location', max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Ambulance Hub'
        verbose_name_plural = 'Ambulance Hubs'

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        AccountType.objects.create(user=self.user, type='ambulance_hub')
        super(AmbulanceHub, self).save(*args, **kwargs)


class Ambulance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User', blank=False, null=False)
    ambulance_no = models.CharField('Ambulance Number', max_length=30, unique=True, blank=False, null=False)
    hub = models.ForeignKey(AmbulanceHub, on_delete=models.CASCADE)
    available = models.BooleanField('Available')

    def __str__(self):
        return self.ambulance_no

    def save(self, *args, **kwargs):
        AccountType.objects.create(user=self.user, type='ambulance')
        super(Ambulance, self).save(*args, **kwargs)
