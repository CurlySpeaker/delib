from django.db import models
from delib.log import Log
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from polymorphic.models import PolymorphicModel, PolymorphicManager

from delib.hashes import sha256

from .roles import ROLES


class UserManager(PolymorphicManager, BaseUserManager):
    use_in_migrations = True

    def create_user(self, pnum, password, **required_args):
        if not pnum or not password:
            raise ValueError("Users must have an pnum and password")

        user = self.model(pnum=pnum, **required_args)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, pnum, password, **required_args):
        user = self.create_user(pnum, password, **required_args)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(PolymorphicModel, AbstractBaseUser):

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    pnum = models.CharField(unique=True, max_length=11)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=3, choices=ROLES)

    # Methods and fields for enabling authentication on this model

    objects = UserManager()

    USERNAME_FIELD = 'pnum'
    REQUIRED_FIELDS = []

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = True

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        return user

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_password(self, raw_password):
        if self.pnum:
            self.password = sha256(self.pnum + raw_password)

    def check_password(self, raw_password):
        return self.password == sha256(self.pnum + raw_password)

    def get_full_name(self):
        return '{0} {1}'.format(self.name, self.surname)

    def get_short_name(self):
        return self.name


class Patron(User):
    class Meta:
        abstract = True


class Faculty(Patron):
    class Meta:
        abstract = True


class Instructor(Faculty):
    pass


class TA(Faculty):
    pass


class Professor(Faculty):
    pass


class Student(Patron):
    pass


class VisitingProfessor(Patron):
    pass


class Admin(User):

    def save(self, *args, **kwargs):
        if Admin.objects.exists() and not self.pk:
            raise ValidationError('There is can be only one Admin in system')
        return super(Admin, self).save(*args, **kwargs)

    @classmethod
    def add_user(cls, Type, **kwargs):
        if issubclass(Type, Librarian):
            Type.objects.create_user(**kwargs)

    def delete_user(self, user):
        if isinstance(user, Librarian):
            user.delete()

    def modify_user(self, user, **kwargs):
        if isinstance(user, Librarian):
            user.update(**kwargs)

    def set_privilege(self, user, privilege=1):
        if isinstance(user, Librarian):
            user.update(privilege=privilege)


def require_previledge(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if user.privilege >= level:
                func()
            else:
                raise ValidationError('Access denied')
        return wrapper
    return decorator


class Librarian(User):
    privilege = models.PositiveIntegerField(default=1)

    @require_previledge(2)
    def add_user(self, Type, **kwargs):
        if issubclass(Type, Patron):
            user = Type.objects.create_user(**kwargs)
            Log.objects.create(text='{1} added {0}'.format(self, user))

    @require_previledge(3)
    def delete_user(self, user):
        if isinstance(user, Patron):
            Log.objects.create(text='{1} deleted {0}'.format(user, self))
            user.delete()

    @require_previledge(1)
    def modify_user(self, user, **kwargs):
        if isinstance(user, Patron):
            user.update(**kwargs)
            Log.objects.create(text='{1} modified {0}'.format(user, self))
