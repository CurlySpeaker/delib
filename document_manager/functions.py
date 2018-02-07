from .models import *

def get_real_document(doc):
	if doc.doc_type == 'bok':
		Model = Book
	elif doc.doc_type == 'ref':
		Model = Reference
	elif doc.doc_type == 'iss':
		Model = Issue
	elif doc.doc_type == 'med':
		Model = Media
	return Model.objects.get(pk=doc.id)

