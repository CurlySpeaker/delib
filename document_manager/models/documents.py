from datetime import date
from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from.author import Author

class Document(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    #TODO think about it
    keywords = models.CharField(max_length=50)
    check_out_period = models.CharField(max_length=1)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    bestseller = models.BooleanField()

    class Meta:
        ordering = ['title']

    @property
    def number_of_copies(self):
        return self.copies.objects.all().count()

    @property
    def number_of_available_copies(self):
        return self.copies.objects.all().filter(LOAN_STATUS='Available').count()

    def check_out(self,user):
        copies = self.copies.objects.filter(status='Available')
        if len(copies) > 0:
            return copies[0].check_out(user)
        else:
            return False

    def __str__(self):
        return '{0} - {1}'.format(self.title,self.authors)


class Book(Document):
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=2)
    year = models.DateField()


class Reference(Book):
    pass


class Journal(Document):
    # No authors here, list of authors will be empty
    publisher = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    editors = models.CharField(max_length=50)
    publication_date = models.DateTimeField(timezone.now())


class JournalArticle(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    journal = models.ForeignKey(Journal,on_delete=models.CASCADE)  # many-to-one


#Audio/Video
class Media(Document):
    pass


'''
document - document to wich copy belongs to
room - position of copy
loaner - by whom checked out
'''
class Copy(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE,related_name='copies')
    room = models.CharField(max_length=50)
    loaner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    time_of_check_out = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('c', 'Checked out'),
        ('a', 'Available'),
        ('r', 'Renewed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='c', help_text='Book availability')

    #Checking out book
    def check_out(self,user):
        if not self.is_available():
            return False
        self.loaner = user
        self.status = 'c'
        self.time_of_check_out = date.today()
        return True

    def is_available(self):
        return self.status == 'a'

    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        return False
''' 
    def set_check_out_period(self):
        if self.document is ReferenceBooksAndMagazines:
            self.check_out_period = 0
        elif self.document is AudioVideo or Journals:
            self.check_out_period = 2
        elif self.is_taken_by_a_faculty_member:
            self.check_out_period = 4
        elif self.document is Books and self.document.is_a_bestseller is True:
            self.check_out_period = 2
        else:
            self.check_out_period = 3
        return self.check_out_period
'''



