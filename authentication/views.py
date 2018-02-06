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


from delib.hashes import sha256

from .forms import (
    AuthorizationForm,
    RegistrationForm,
)
from django.contrib.auth import get_user_model
User = get_user_model()

from user_manager.models import Faculty, Student, Librarian


def redirect_if_authorized(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/docs/')
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
                return HttpResponseRedirect('/docs/')
            else:
                form.add_error(None, "User doesn't exist")
    else:
        form = AuthorizationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login')


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
            user_type = form.cleaned_data['user_type']
            if User.objects.filter(pnum=pnum).exists():
                form.add_error('pnum', "Phone number already in use")
            else:
                is_superuser = False
                is_staff = False
                if user_type == 'student':
                    Model = Student
                elif user_type == 'faculty':
                    Model = Faculty
                else:
                    Model = Librarian
                    is_superuser = True
                    is_staff = True
                user = Model.objects.create_user(pnum=pnum,password=password,name=name,surname=surname,address=address, is_staff=is_staff, is_superuser=is_superuser)
                user.save()
                return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()

    return render(request, 'authentication/registration.html', {'form': form})