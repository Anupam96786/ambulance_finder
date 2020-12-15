from django.contrib import admin
from .models import Users, Ambulance, Ambulance_hub

admin.site.register(Users)
admin.site.register(Ambulance)
admin.site.register(Ambulance_hub)
