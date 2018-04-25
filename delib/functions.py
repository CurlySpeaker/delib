from delib.models import Log
from document_manager.models import *
from user_manager.models import *


def check_system(user):
    Log.objects.create(text='{0} checked the system'.format(user))
    docs = ['{0} # of copies:{1}'.format(doc, doc.number_of_copies) for doc in
            Document.objects.all()]
    patrons = Patron.objects.all()
    return 'Documents:\n {0} \nPatrons:\n {1}'.format(docs, patrons)
