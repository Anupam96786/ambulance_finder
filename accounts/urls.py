from django.urls import path
from . import views

urlpatterns = [
    path('users/signup/', views.CreateUser.as_view()),
    path('useractivation/<str:token>', views.UserActivation.as_view()),
]
