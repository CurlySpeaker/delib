from .models import Faculty, Librarian, Student


def get_real_user(user):
    if user.user_type == 'fac':
        Model = Faculty
    elif user.user_type == 'stu':
        Model = Student
    else:
        Model = Librarian
    return Model.objects.get(pk=user.id)
