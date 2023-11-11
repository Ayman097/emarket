from django.urls import path
from . import views

urlpatterns = [
    path('register/',  views.register, name='register'),
    path('user/',  views.current_user, name='user'),
    path('user/update',  views.update_user, name='user'),
    path('forget_password/',  views.forget_password, name='forget_password'),
    path('reset_password/<str:token>',  views.reset_password, name='reset_password'),
]