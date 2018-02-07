from django.test import TestCase
import datetime
from user_manager.models import *
from document_manager.models import *

class TestCases(TestCase):
    def setUp(self):
    	pass

    def test_1(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(student)
    	print(Copy.objects.filter(loaner=student))
    	print(Copy.objects.filter(document=book,status='a'))

    def test_2(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	try:
    		Book.objects.filter(authors=Author.objects.all()).first().check_out(student)
    	except:
    		print('No such book')
    	else:
    		pass
    	print('student copies:',Copy.objects.filter(loaner=student))

    def test_3(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	faculty = Faculty.objects.create_user(pnum='00000000002', password='innopolis1', user_type='fac')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(faculty)
    	print(book.check_out_period(faculty))

    def test_4(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	faculty = Faculty.objects.create_user(pnum='00000000002', password='innopolis1', user_type='fac')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10), is_bestseller=True)
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(faculty)
    	print(book.check_out_period(faculty))
 
    def test_5(self):
    	student1 = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	student2 = Student.objects.create_user(pnum='00000000004', password='innopolis1', user_type='stu')
    	student3 = Student.objects.create_user(pnum='00000000005', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	print(book.check_out(student1))
    	print(book.check_out(student2))
    	print(book.check_out(student3))

    def test_6(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(student)
    	print(Copy.objects.filter(loaner=student))
    	book.check_out(student)
    	print(Copy.objects.filter(loaner=student))
    	print(Copy.objects.filter(status='a'))
  
    def test_7(self):
    	student1 = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	student2 = Student.objects.create_user(pnum='00000000002', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	print(Copy.objects.filter(document=book,status='a'))
    	print(book.check_out(student1))
    	print(book.check_out(student2))
    	print(Copy.objects.filter(document=book,status='a'))

    def test_8(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	faculty = Faculty.objects.create_user(pnum='00000000002', password='innopolis1', user_type='fac')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(student)
    	print(book.check_out_period(student))

    def test_9(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	faculty = Faculty.objects.create_user(pnum='00000000002', password='innopolis1', user_type='fac')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10), is_bestseller=True)
    	copy1 = Copy.objects.create(document=book)
    	copy2 = Copy.objects.create(document=book)

    	book.check_out(student)
    	print(book.check_out_period(student))

    def test_10(self):
    	student = Student.objects.create_user(pnum='00000000000', password='innopolis1', user_type='stu')
    	librarian = Librarian.objects.create_user(pnum='00000000001',password='innopolis1',user_type='lib',is_superuser=True, is_staff=True)
    	author = Author.objects.create(name='Newton')
    	key_word = Keyword.objects.create(word='science')
    	book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	reference = Book.objects.create(title='Designed By Contract', price=10, doc_type='ref', publisher='moscow', edition='1', year=datetime.date(1999,10,10))
    	copy1 = Copy.objects.create(document=reference)
    	copy2 = Copy.objects.create(document=book)

    	print(copy1.check_out(student))
    	print(copy2.check_out(student))
  