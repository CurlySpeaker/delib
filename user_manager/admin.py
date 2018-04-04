from django.contrib import admin


from .models.user import User, Student, Librarian, VisitingProfessor, Professor, TA, Instructor

admin.site.register([User, Student, Librarian, VisitingProfessor, Professor, TA, Instructor])
