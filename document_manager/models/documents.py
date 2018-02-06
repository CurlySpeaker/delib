from datetime import date, timedelta
from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from.author import Author


class Keyword(models.Model):
    word = models.CharField(max_length=20)


class Document(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    keywords = models.ManyToManyField(Keyword)
    #TODO think about it
    def check_out_period():
        pass

    price = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        ordering = ['title']

    @property
    def number_of_copies(self):
        return self.copies.all().count()

    @property
    def available_copies(self):
        return self.copies.filter(status='a')

    def check_out(self, user):
        if len(self.copies.filter(loaner=user)) > 0:
            return False
        copies = self.available_copies
        if len(copies) > 0:
            return copies[0].check_out(user)
        else:
            return False

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.authors)


class Book(Document):
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=2)
    year = models.DateField()
    is_bestseller = models.BooleanField()
    def check_out_period(user):
        if isinstance(user, Faculty):
            return 28
        elif is_bestseller:
            return 14:
        else:
            return 21


class Reference(Book):
    pass


class Journal(models.Model):
    publisher = models.CharField(max_length=50)


class Issue (Document):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='issues')
    editors = models.ManyToManyField(Editors, on_delete = models.DO_NOTHING)
    publication_date = models.DateTimeField(timezone.now())
    def check_out_period(user):
        return 14
    @property
    def authors(): 
        pass



class JournalArticle(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='journal_articles')  # many-to-one


#Audio/Video
class Media(Document):
    pass


'''
document - document to wich copy belongs to
room - position of copy
loaner - by whom checked out
'''
class Copy(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='copies')
    room = models.CharField(max_length=50)
    loaner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booking_time = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('c', 'Checked out'),
        ('a', 'Available'),
        ('r', 'Renewed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='c', help_text='Book availability')

    #Checking out book
    def check_out(self, user):
        if not self.is_available():
            return False
        self.loaner = user
        self.status = 'c'
        self.booking_time = date.today()
        self.save()
        return True

    def is_available(self):
        return self.status == 'a'

    def is_overdue(self):
        if (date.today() - self.booking_time()).day() > self.document.check_out_period(self.loaner):
            return True
        return False