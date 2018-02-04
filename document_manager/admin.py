from django.contrib import admin

from .models import Document, Author

admin.site.register([Document,Author])
