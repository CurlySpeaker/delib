from .models import Faculty, Librarian, Student, VisitingProfessor


def get_real_user(user):
    if user.user_type == 'fac':
        Model = Faculty
    elif user.user_type == 'stu':
        Model = Student
    elif user.user_type == 'vp':
        Model = VisitingProfessor
    else:
        Model = Librarian
    return Model.objects.get(pk=user.id)
