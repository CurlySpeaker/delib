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
    user = {'id':request.user.id, 'name':request.user.get_full_name()}
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
            return HttpResponse('No copies')