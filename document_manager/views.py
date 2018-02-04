from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    Http404,
)

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Document


def require_authorized(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        return function(request, *args, **kwargs)
    return wrapper


@require_authorized
def index(request):
    all_books = {}
    documents = Document.objects.all()
    docs = [{'id': doc.id, 'title': doc.title} for doc in documents]
    print(docs)
    return render(request, 'document_manager/index.html', {'docs': docs})

@require_authorized
def book(request):
    pass