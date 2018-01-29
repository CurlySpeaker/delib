from datetime import date

from django.db import models
from django.utils import timezone


class Documents(models.Model):
    title = models.CharField(max_length=50)
    list_of_authors = models.ForeignKey('Authors',on_delete=models.CASCADE)
    list_of_keywords = models.CharField(max_length=50)

    check_out_time = models.DurationField()
    price = models.DecimalField(decimal_places=2,max_digits=6)
    copies = models.ForeignKey('Copies',on_delete=models.CASCADE)
    number_of_copies = models.SmallIntegerField()
    number_of_available_copies = models.SmallIntegerField()

    class Meta:
        abstract = True
        ordering = ["title"]
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title + "-" + self.list_of_authors


class Books(Documents):
    publisher = models.CharField(max_length=50)
    edition = models.SmallIntegerField()
    year = models.DateField()
    is_a_bestseller = models.BooleanField()
    is_taken_by_a_faculty_member = models.BooleanField()


class ReferenceBooksAndMagazines(Books):
    def set_check_out_time(self):
        self.check_out_time = 0


class JournalArticles(models.Model):
    title = models.CharField(max_length=50)
    list_of_authors = models.CharField(max_length=50)
    journal = models.ForeignKey('Journals',on_delete=models.CASCADE)  # many-to-one


class Journals(Documents):
    # No authors here, list of authors will be empty
    publisher = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    editors = models.CharField(max_length=50)
    publication_date = models.DateTimeField(timezone.now())

    def set_check_out_time(self):
        self.check_out_time = 2


class AudioVideo(Documents):
    def set_check_out_time(self):
        self.check_out_time = 2


class Copies(models.Model):
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    is_checked_out = models.BooleanField()
    checked_out_by = models.ForeignKey('User',on_delete=models.CASCADE)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('c', 'Checked out'),
        ('a', 'Available'),
        ('r', 'Renewed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Book availability')

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Authors(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

