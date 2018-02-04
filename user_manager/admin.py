from django.contrib import admin


from .models.user import User, Faculty, Student, Librarian

admin.site.register([User,Faculty,Student, Librarian])
