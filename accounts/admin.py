from django.contrib import admin
from .models import Users, Ambulance, AmbulanceHub, AccountType

admin.site.register(Users)

@admin.register(Ambulance)
class Account(admin.ModelAdmin):
    list_display = ['user', 'ambulance_no', 'hub']

@admin.register(AmbulanceHub)
class Account(admin.ModelAdmin):
    list_display = ['user', 'name']

@admin.register(AccountType)
class Account(admin.ModelAdmin):
    list_display = ['user', 'type']
