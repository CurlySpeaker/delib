from user_manager.models import *
from user_manager.functions import get_real_user
from datetime import date
import datetime

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from django.contrib.auth import get_user_model
User = get_user_model()

from.author import Author, Editor


class Keyword(models.Model):
    word = models.CharField(max_length=20)


class Document(PolymorphicModel):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    keywords = models.ManyToManyField(Keyword)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        ordering = ['title']

    '''
    cheking out system
    '''
    @property
    def number_of_copies(self):
        return self.copies.all().count()

    @property
    def available_copies(self):
        return self.copies.filter(status='a')

    def have_copy(self, user):
        return self.copies.filter(loaner=user).exists()

    def check_out(self, user):
        if self.have_copy(user):
            return False
        copies = self.available_copies
        if len(copies) > 0:
            return copies[0].check_out(user)
        else:
            return False

    def check_out_period(self, user):
        pass

    '''
    doc add/delete/modfy
    '''
    @classmethod
    def add_doc(cls, user, **kwargs):
        if isinstance(user, Librarian):
            cls.objects.create(**kwargs)

    def modify_doc(self, user):
        if isinstance(user, Librarian):
            self.update(**kwargs)

    def remove_doc(self, user):
        if isinstance(user, Librarian):
            self.delete()

    def add_copy(self, user, ammount=1, **kwargs):
        if isinstance(user, Librarian):
            for i in range(ammount):
                Copy.objects.create(document=self, **kwargs)

    def remove_copy(self, user, ammount=1):
        if isinstance(user, Librarian):
            for i in range(ammount):
                try:
                    Copy.objects.filter(document=self)[0].delete()
                except:
                    return False

    # return doc
    def return_doc(self, user):
        if not self.have_copy(user):
            return False
        copy = self.copies.filter(loaner=user)[0]
        return copy.return_copy()

    def __str__(self):
        return '{0}'.format(self.title)


class Book(Document):
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=2)
    year = models.DateField()
    is_bestseller = models.BooleanField(default=False)

    def check_out_period(self, user):
        if isinstance(user, Faculty):
            return 28
        elif self.is_bestseller:
            return 14
        else:
            return 21


class Reference(Book):
    pass


class Journal(models.Model):
    publisher = models.CharField(max_length=50)


class Issue (Document):
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name='issues')
    editors = models.ManyToManyField(Editor)
    publication_date = models.DateTimeField(timezone.now())

    def check_out_period(self, user):
        return 14

    @property
    def authors(self):
        pass


class JournalArticle(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE,
        related_name='journal_articles')  # many-to-one


# Audio/Video
class Media(Document):

    def check_out_period(self,user):
        return 14


'''
document - document to wich copy belongs to
room - position of copy
loaner - by whom checked out
'''


class Copy(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='copies')
    room = models.CharField(max_length=50, blank=True)
    loaner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    booking_time = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('c', 'Checked out'),
        ('a', 'Available'),
        ('r', 'Renewed'),
    )

    status = models.CharField(
        max_length=1, choices=LOAN_STATUS,
        default='a', help_text='Book availability')

    # Checking out book
    def check_out(self, user):
        if not self.is_available():
            return False
        if isinstance(self.document, Reference):
            return False
        self.loaner = user
        self.status = 'c'
        self.booking_time = date.today()
        self.save()
        return True

    def is_available(self):
        return self.status == 'a'

    def checked_due(self):
        return (self.booking_time +
                datetime.timedelta(days=self.document.check_out_period(get_real_user(self.loaner))))

    def is_overdue(self):
        if (date.today() - self.booking_time()).day() \
           > self.document.check_out_period(self.loaner):
            return True
        return False

    def return_copy(self):
        self.status = 'a'
        self.booking_time = None
        self.loaner = None
        self.save()
        return True
