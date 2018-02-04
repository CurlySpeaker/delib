from django.contrib import admin

from .models import Document, Author, Copy, Book

admin.site.register([Document,Author, Copy, Book])
