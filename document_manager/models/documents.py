'''
from datetime import date
from django.db import models
from django.utils import timezone


class Documents(models.Model):
    title = models.CharField(max_length=50)
    list_of_authors = models.ManyToManyField('authors')
    list_of_keywords = models.CharField(max_length=50)

    check_out_period = models.CharField(max_length=1)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    copies = models.ForeignKey('copies',on_delete=models.CASCADE)
    number_of_copies = models.SmallIntegerField()
    is_a_bestseller = models.BooleanField()

    @property
    def number_of_copies(self):
        return self.copies.objects.all().count()

    @property
    def number_of_available_copies(self):
        return self.copies.objects.all().filter(LOAN_STATUS='Available').count()

    class Meta:
        abstract = True
        ordering = ["title"]

    def __str__(self):
        return "{0} - {1}".format(self.title,self.list_of_authors)


class Books(Documents):
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=2)
    year = models.DateField()


class ReferenceBooksAndMagazines(Books):
    pass


class JournalArticles(models.Model):
    title = models.CharField(max_length=50)
    list_of_authors = models.ForeignKey('authors',on_delete=models.CASCADE)
    journal = models.ForeignKey('journals',on_delete=models.CASCADE)  # many-to-one


class Journals(Documents):
    # No authors here, list of authors will be empty
    publisher = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    editors = models.CharField(max_length=50)
    publication_date = models.DateTimeField(timezone.now())


class AudioVideo(Documents):
    pass


class Copies(models.Model):
    document = models.ForeignKey(Documents,on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    checked_out_by = models.ForeignKey('user',on_delete=models.CASCADE)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('c', 'Checked out'),
        ('a', 'Available'),
        ('r', 'Renewed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Book availability')

    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        return False
    
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


class Authors(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

'''