from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
)
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)


from .forms import (
    AuthorizationForm,
    RegistrationForm,
)

from user_manager.models import (
    User,
    Faculty,
    Student,
    Librarian,
)

def redirect_if_authorized(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
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
                return HttpResponseRedirect(reverse('home'))
            else:
                form.add_error(None, "User doesn't exist")
    else:
        form = AuthorizationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('login'))


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
                    user_type = 'stu'
                elif user_type == 'faculty':
                    Model = Faculty
                    user_type = 'fac'
                elif user_type == 'vp':
                    Model = VisitingProfessor
                    user_type = 'vp'
                else:
                    user_type = 'lib'
                    Model = Librarian
                    is_superuser = True
                    is_staff = True
                user = Model.objects.create_user(pnum=pnum,
                                                 password=password,
                                                 name=name,
                                                 surname=surname,
                                                 address=address,
                                                 is_staff=is_staff,
                                                 is_superuser=is_superuser,
                                                 user_type=user_type)
                user.save()
                return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()

    return render(request, 'authentication/registration.html', {'form': form})
