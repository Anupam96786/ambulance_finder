from django.contrib import admin
from .models import Users, Ambulance, AmbulanceHub, AccountType

admin.site.register(Users)
admin.site.register(Ambulance)
admin.site.register(AmbulanceHub)
admin.site.register(AccountType)
