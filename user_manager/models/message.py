from django.db import models
from .user import *

notifications = {
    'available' : 'Dear, {user}, {doc} is now available, you can book it.',
    'return' : 'Dear, {user}, please return {doc}.',
    'unavailable': 'Dear, {user}, {doc} is now unavailable. You have been removed from waiting list',
}

class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages',
                             on_delete=models.CASCADE)
    text = models.TextField()


    @classmethod
    def send_message(cls, user, notification, document):
        cls.objects.create(user=user,
                          text=notifications[notification].format(
                              user=user.name,
                              doc=document.title,
                          )
                          )

    def __str__(self):
        return '{0}'.format(self.text)
