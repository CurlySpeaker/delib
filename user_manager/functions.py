from .models import Faculty, Librarian, Student, VisitingProfessor

def require_previledge(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if user.privilege >= level:
                func()
            else:
                raise ValidationError('You do not have privilege for this action')
        return wrapper
    return decorator


