from django.urls import path
from document_manager import views as doc_view

urlpatterns = [
    path('', doc_view.index, name='home'),
    path('my_books/', doc_view.my_books, name='my_books'),
    path('book/<int:id>', doc_view.book, name='book'),
    path('return_doc/<int:id>', doc_view.return_doc, name='return_doc'),
]
