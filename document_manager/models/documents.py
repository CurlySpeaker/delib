from user_manager.models import (
    Librarian,
    Student,
    VisitingProfessor,
    Professor,
    Faculty,
    TA,
    Instructor,

    Message,

    require_previledge,
)
from delib.models import Log
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
    is_outstanding = models.BooleanField(default=False)
    waiting_list = models.ManyToManyField(User, blank=True)

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
        if self.is_outstanding:
            return False
        if len(copies) > 0:
            Log.objects.create(text='{0} checked out {1}'.format(user, self.title))
            return copies[0].check_out(user)
        elif user in self.waiting_list.all():
            return False
        self.waiting_list.add(user)
        Log.objects.create(text='{0} checked out {1}'.format(user, self.title))
        self.save()

    def check_out_period(self, user):
        pass

    @classmethod
    @require_previledge(2)
    def add_doc(cls, user, **kwargs):
        if isinstance(user, Librarian):
            doc = cls.objects.create(**kwargs)
            Log.objects.create(text='{0} created {1}'.format(user, doc))

    def modify_doc(self, user, **kwargs):
        if isinstance(user, Librarian):
            self.update(**kwargs)
            Log.objects.create(text='{0} modified {1}'.format(user, self))

    @require_previledge(3)
    def remove_doc(self, user):
        if isinstance(user, Librarian):
            Log.objects.create(text='{0} removed {1}'.format(user, self))
            self.delete()

    @require_previledge(2)
    def outstanding(self, user, make_outstanding=True):
        if isinstance(user, Librarian):
            self.is_outstanding = make_outstanding
            if not make_outstanding:
                return True
            for use in self.get_waiting_list():
                Message.send_message(
                    user=use, notification='unavailable', document=self)
            self.waiting_list.clear()
            Log.objects.create(text='Waiting list of {0} was cleared'.format(self))
            users = [i.loaner for i in self.copies.all()
                     if i.loaner is not None]
            for use in users:
                Message.send_message(
                    user=use, notification='return', document=self)
            for copy in self.copies.all():
                if copy.status == 'c' or copy.status == 'r':
                    copy.booking_time = date.today(
                    ) - datetime.timedelta(days=self.check_out_period(copy.loaner))
                    copy.save()
            self.save()
            Log.objects.create(
                text='{0} made outstanding {1}'.format(user, self))

    @require_previledge(2)
    def add_copy(self, user, ammount=1, **kwargs):
        if isinstance(user, Librarian):
            for i in range(ammount):
                Copy.objects.create(document=self, **kwargs)
            Log.objects.create(text='{0} made {2} copies of  {1}'.format(user,
                                                                         self,
                                                                         ammount))

    @require_previledge(3)
    def remove_copy(self, user, ammount=1):
        if isinstance(user, Librarian):
            for i in range(ammount):
                try:
                    Copy.objects.filter(document=self)[0].delete()
                except:
                    return False
                else:
                    Log.objects.create(text='{0} deleted {2} copies of \
                                       {1}'.format(user, self, ammount))

    def get_waiting_list(self):
        waiting = []
        for i in [Student, Instructor, TA, VisitingProfessor, Professor]:
            for j in self.waiting_list.all():
                if isinstance(j, i):
                    waiting.append(j)
        return waiting

    def return_doc(self, user):
        if not self.have_copy(user):
            return False
        copy = self.copies.filter(loaner=user)[0]
        waiting_list = self.get_waiting_list()
        if len(waiting_list) > 0:
            Message.send_message(user=waiting_list[0], notification='available',
                                 document=self)
        Log.objects.create(text='{0} returned {1}'.format(user, self))
        return copy.return_copy()

    def renew_doc(self, user):
        if not self.have_copy(user):
            return False
        if self.is_outstanding:
            return False
        copy = self.copies.filter(loaner=user)[0]
        if copy.renew_copy(user):
            Log.objects.create(text='{0} renewed {1}'.format(user, self))
            return True
        return False

    def get_fine(self, user):
        if not self.have_copy(user):
            return False
        copy = self.copies.filter(loaner=user)[0]
        return copy.get_fine()

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
        elif isinstance(user, VisitingProfessor):
            return 7
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
        related_name='journal_articles')


class Media(Document):

    def check_out_period(self, user):
        if isinstance(user, VisitingProfessor):
            return 7
        return 14


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
                datetime.timedelta(days=self.document.check_out_period(self.loaner)))

    def is_overdue(self):
        return self.get_overdue() > 0

    def renew_copy(self, user):
        if isinstance(user, VisitingProfessor) or self.status == 'c':
            self.status = 'r'
            self.booking_time = date.today()
            self.save()
            return True
        else:
            return False

    def return_copy(self):
        self.status = 'a'
        self.booking_time = None
        self.loaner = None
        self.save()
        return True

    def get_overdue(self):
        overdue = (date.today() - self.booking_time).days - \
            self.document.check_out_period(self.loaner)
        return overdue if overdue > 0 else 0

    def get_fine(self):
        if not self.is_overdue():
            return 0
        else:
            fine = 100.00 * self.get_overdue()
            return fine if fine < self.document.price else float(self.document.price)


def search(user, title=None, keyword=None):
    docs = Document.objects.all()
    if title is not None:
        result = []
        for i in docs:
            if title in i.title:
                result.append(i)
    if keyword is not None:
        result = []
        for i in docs:
            for j in i.keywords.all():
                if keyword == j.word:
                    result.append(i)
    return result
