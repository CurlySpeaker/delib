from django.db import models
from django.utils.timezone import now


class Log(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=now())

    def __str__(self):
        return '{0} : {1}'.format(self.date, self.text)
