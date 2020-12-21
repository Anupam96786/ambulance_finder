from django.contrib import admin
from .models import Users, Ambulance, AmbulanceHub, AccountType, Token

admin.site.register(Users)

@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'ambulance_no', 'hub']

@admin.register(AmbulanceHub)
class AmbulanceHubAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'purpose']
