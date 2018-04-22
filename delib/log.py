from django.db import models
from datetime import date


def log(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func()
            Log.objects.create(text=text, date=date.today())
        return wrapper
    return decorator


class Log(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=date.today())
