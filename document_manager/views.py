from .models import Document, Copy
from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)

from django.contrib.auth import get_user_model
User = get_user_model()


def require_authorized(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        return function(request, *args, **kwargs)
    return wrapper


@require_authorized
def index(request):
    documents = Document.objects.all()
    user = {'id': request.user.id, 'name': request.user.get_full_name(),
            'pnum': request.user.pnum}
    docs = [{'id': doc.id, 'title': doc.title, 'authors': [
        author for author in doc.authors.all()]} for doc in documents]
    return render(request, 'document_manager/index.html', {'docs': docs, 'user': user})


@require_authorized
def book(request, id):
    user = User.objects.get(pk=request.user.id)
    try:
        doc = Document.objects.get(pk=id)
    except:
        return HttpResponse('No such book')
    else:
        if doc.check_out(user):
            return HttpResponse('Success')
        else:
            return HttpResponse('No copies or you have one')


@require_authorized
def my_books(request):
    copies = Copy.objects.filter(
        loaner=User.objects.get(pk=request.user.id))
    user = {'id': request.user.id, 'name': request.user.get_full_name(),
            'pnum': request.user.pnum}
    documents = [doc.document for doc in copies]
    docs = [{'id': doc.id, 'title': doc.title, 'authors': [
        author for author in doc.authors.all()]} for doc in documents]
    return render(request, 'document_manager/my_books.html', {'docs': docs, 'user': user})


@require_authorized
def return_doc(request, id):
    user = User.objects.get(pk=request.user.id)
    try:
        doc = Document.objects.get(pk=id)
    except:
        return HttpResponse('No such book')
    else:
        if doc.return_doc(user):
            return HttpResponse('Success')
        else:
            return HttpResponse('You do not have this doc')
