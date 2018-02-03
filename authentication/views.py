from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    Http404,
)
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)


from hashlib import sha256

from user_manager.models import User
from .forms import (
    AuthorizationForm,
    RegistrationForm,
    SubscribeForm,
)


def redirect_if_authorized(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/account/')
        return function(request, *args, **kwargs)
    return wrapper


@redirect_if_authorized
def login(request):
    if request.method == 'POST':  
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = django_authenticate(
                request,
                pnum=form.cleaned_data['pnum'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "User doesn't exist")
    else:
        form = AuthorizationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')


@redirect_if_authorized
def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            pnum = form.cleaned_data['pnum']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            address = form.cleaned_data['address']
            
            if User.objects.filter(pnum=pnum).exists():
                form.add_error('pnum', "Phone number already in use")
            else:
                user = User.create_user(pnum,password,name=name,surname=surname,patronymics=patronymics,address=address)
                user.save()
                return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()

    return render(request, 'authentication/registration.html', {'form': form})