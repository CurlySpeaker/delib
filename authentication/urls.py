from django.urls import path
from authentication import views as auth_view

urlpatterns = [
    path('login/', auth_view.login, name='login'),
    path('logout/', auth_view.logout, name='logout'),
    path('register/', auth_view.register, name='register'),
]
