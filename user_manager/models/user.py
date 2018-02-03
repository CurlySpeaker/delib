from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from  hashlib import sha256


class UserManager(BaseUserManager):

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


class User(AbstractBaseUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    pnum = models.CharField(unique=True, max_length=11)
    password = models.CharField(max_length=128)

    # Methods and fields for enabling authentication on this model

    objects = UserManager()

    USERNAME_FIELD = 'pnum'
    REQUIRED_FIELDS = []

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = True

    class Meta:
        abstract = True


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
    abstract = True



class Faculty(Patron):
    pass


class Student(Patron):
    pass


class Librarian(User):
    pass