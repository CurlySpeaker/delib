from django.test import TestCase
import os
import datetime
from user_manager.models import *
from document_manager.models import *
from delib.functions import check_system


class TestCase1(TestCase):
    def setUp(self):
        pass

    def test_1(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(student)
        print(Copy.objects.filter(loaner=student))
        print(Copy.objects.filter(document=book, status='a'))

    def test_2(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        try:
            Book.objects.filter(authors=Author.objects.all()
                                ).first().check_out(student)
        except:
            print('No such book')
        else:
            pass
        print('student copies:', Copy.objects.filter(loaner=student))

    def test_3(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        faculty = Faculty.objects.create_user(
            pnum='00000000002', password='innopolis1', user_type='fac')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(faculty)
        print(book.check_out_period(faculty))

    def test_4(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        faculty = Faculty.objects.create_user(
            pnum='00000000002', password='innopolis1', user_type='fac')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow',
                                   edition='1', year=datetime.date(1999, 10, 10), is_bestseller=True)
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(faculty)
        print(book.check_out_period(faculty))

    def test_5(self):
        student1 = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        student2 = Student.objects.create_user(
            pnum='00000000004', password='innopolis1', user_type='stu')
        student3 = Student.objects.create_user(
            pnum='00000000005', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        print(book.check_out(student1))
        print(book.check_out(student2))
        print(book.check_out(student3))

    def test_6(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(student)
        print(Copy.objects.filter(loaner=student))
        book.check_out(student)
        print(Copy.objects.filter(loaner=student))
        print(Copy.objects.filter(status='a'))

    def test_7(self):
        student1 = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        student2 = Student.objects.create_user(
            pnum='00000000002', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        print(Copy.objects.filter(document=book, status='a'))
        print(book.check_out(student1))
        print(book.check_out(student2))
        print(Copy.objects.filter(document=book, status='a'))

    def test_8(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        faculty = Faculty.objects.create_user(
            pnum='00000000002', password='innopolis1', user_type='fac')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(student)
        print(book.check_out_period(student))

    def test_9(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        faculty = Faculty.objects.create_user(
            pnum='00000000002', password='innopolis1', user_type='fac')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok', publisher='moscow',
                                   edition='1', year=datetime.date(1999, 10, 10), is_bestseller=True)
        copy1 = Copy.objects.create(document=book)
        copy2 = Copy.objects.create(document=book)

        book.check_out(student)
        print(book.check_out_period(student))

    def test_10(self):
        student = Student.objects.create_user(
            pnum='00000000000', password='innopolis1', user_type='stu')
        librarian = Librarian.objects.create_user(
            pnum='00000000001', password='innopolis1', user_type='lib', is_superuser=True, is_staff=True)
        author = Author.objects.create(name='Newton')
        key_word = Keyword.objects.create(word='science')
        book = Book.objects.create(title='Starts', price=10, doc_type='bok',
                                   publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        reference = Book.objects.create(title='Designed By Contract', price=10, doc_type='ref',
                                        publisher='moscow', edition='1', year=datetime.date(1999, 10, 10))
        copy1 = Copy.objects.create(document=reference)
        copy2 = Copy.objects.create(document=book)

        print(copy1.check_out(student))
        print(copy2.check_out(student))


class TestCase2(TestCase):
    def setUp(self):
        self.librarian = Librarian.objects.create_user(
            pnum='0000000000', password='kek1', user_type='lib',
            is_superuser=True, is_staff=True)

        authors = [Author.objects.create(name='Thomas H. Cormen'),
                   Author.objects.create(name='Charles E. Leiserson'),
                   Author.objects.create(name='Ronald L. Rivest'),
                   Author.objects.create(name='Clifford Stein')
                   ]
        self.b1 = Book.objects.create(
            title='Introduction to Algorithms',
            publisher='MIT press',
            year=datetime.date(2009, 10, 10),
            edition='Third edition',
            price=100,
        )
        self.b1.authors.set(authors)

        authors = [Author.objects.create(name='Erich Gamma'),
                   Author.objects.create(name='Ralph Johnson'),
                   Author.objects.create(name='John Vlisidos'),
                   Author.objects.create(name='Richard Helm')
                   ]
        self.b2 = Book.objects.create(
            title='Design Patterns: Elements of '
            'Reusable Object-Oriented Software',
            publisher='Addison-Wesley Professional',
            year=datetime.date(2003, 10, 10),
            edition="First edition",
            price=100,
            is_bestseller=True,
        )
        self.b1.authors.set(authors)

        authors = [Author.objects.create(name='Brooks'),
                   Author.objects.create(name='Jr'),
                   Author.objects.create(name='Frederick P'),
                   ]
        self.b3 = Reference.objects.create(
            title='The Mythical Man-month',
            publisher='Addison-Wesley Longman Publishing Co., Inc.',
            year=datetime.date(1995, 10, 10),
            edition="Second edition",
            price=100,
        )
        self.b3.authors.set(authors)

        author = [Author.objects.create(name='Tony Huare')]
        self.av1 = Media.objects.create(title='Null References: '
                                        'The Billion Dollar Mistake',
                                        price=100,
                                        )
        self.av1.authors.set(author)

        author = [Author.objects.create(name='Claude Shannon')]
        self.av2 = Media.objects.create(title='Information Entropy',
                                        price=100,
                                        )
        self.av2.authors.set(author)

    def test1(self):
        self.b1.add_copy(self.librarian, ammount=3)
        self.b2.add_copy(self.librarian, ammount=2)
        self.b3.add_copy(self.librarian, ammount=1)
        self.av1.add_copy(self.librarian)
        self.av2.add_copy(self.librarian)
        self.librarian.add_user(Type=Faculty,
                                user_type='fac',
                                name='Sergey',
                                surname='Afonso',
                                address='Via Margutta, 3',
                                pnum='30001',
                                password='innopolis1')
        self.librarian.add_user(Type=Student,
                                user_type='stu',
                                name='Nadia',
                                surname='Teixeira',
                                address='Via Sacra, 13',
                                pnum='30002',
                                password='innopolis1')
        self.librarian.add_user(Type=Student,
                                user_type='stu',
                                name='Elvira',
                                surname='Espindola',
                                address='Via del Corso, 22',
                                pnum='30003',
                                password='innopolis1')
        self.assertEqual(len(User.objects.all()), 4)
        self.assertEqual(len(Copy.objects.all()), 8)

    def test2(self):
        self.test1()
        self.b1.remove_copy(self.librarian, ammount=2)
        self.b3.remove_copy(self.librarian, ammount=1)
        self.librarian.delete_user(User.objects.filter(pnum='30002'))
        self.assertEqual(len(User.objects.all()), 3)
        self.assertEqual(len(Copy.objects.all()), 5)

    def get_info(self, user):
        copies = Copy.objects.filter(loaner=user)
        docs = {copy.document: copy.checked_due() for copy in copies}
        return{
            'name': user.get_full_name(),
            'adress': user.address,
            'pnum': user.pnum,
            'card_id': user.pnum,
            'type': user.user_type,
            'docs': docs,
        }

    def test3(self):
        self.test1()
        print(self.get_info(User.objects.filter(pnum='30001').get()))
        print(self.get_info(User.objects.filter(pnum='30003').get()))

    def test4(self):
        self.test2()
        try:
            print(self.get_info(User.objects.filter(pnum='30002').get()))
        except:
            print('No such user')
        try:
            print(self.get_info(User.objects.filter(pnum='30003').get()))
        except:
            print('No such user')

    def test5(self):
        self.test2()
        try:
            self.b1.check_out(User.objects.filter(pnum='30002').get())
        except User.DoesNotExist:
            print('No such user')

    def test6(self):
        self.test2()
        self.b1.check_out(get_real_user(
            User.objects.filter(pnum='30001').get()))
        self.b1.check_out(get_real_user(
            User.objects.filter(pnum='30003').get()))
        self.b2.check_out(get_real_user(
            User.objects.filter(pnum='30001').get()))
        print(self.get_info(get_real_user(User.objects.filter(pnum='30001').get())))
        print(self.get_info(get_real_user(User.objects.filter(pnum='30003').get())))

    def test7(self):
        self.test1()
        self.b1.check_out(User.objects.filter(pnum='30001').get())
        self.b2.check_out(User.objects.filter(pnum='30001').get())
        self.b3.check_out(User.objects.filter(pnum='30001').get())
        self.av1.check_out(User.objects.filter(pnum='30001').get())

        self.b1.check_out(User.objects.filter(pnum='30002').get())
        self.b2.check_out(User.objects.filter(pnum='30002').get())
        self.av2.check_out(User.objects.filter(pnum='30002').get())
        print(self.get_info(get_real_user(User.objects.filter(pnum='30001').get())))
        print(self.get_info(get_real_user(User.objects.filter(pnum='30002').get())))

    def test8(self):
        self.test1()
        self.b1.check_out(User.objects.filter(pnum='30001').get())
        c1 = Copy.objects.filter(loaner=User.objects.filter(
            pnum='30001')[0], document=self.b1)[0]
        c1.booking_time = datetime.date(year=2018, month=2, day=9)
        c1.save()
        self.b2.check_out(User.objects.filter(pnum='30001').get())
        c2 = Copy.objects.filter(loaner=User.objects.filter(
            pnum='30001').get()).filter(document=self.b2).get()
        c2.booking_time = datetime.date(year=2018, month=2, day=2)
        c2.save()

        self.b1.check_out(User.objects.filter(pnum='30002').get())
        c3 = Copy.objects.filter(loaner=User.objects.filter(
            pnum='30002')[0]).filter(document=self.b1).get()
        c3.booking_time = datetime.date(year=2018, month=2, day=5)
        c3.save()
        self.av1.check_out(User.objects.filter(pnum='30002').get())
        c4 = Copy.objects.filter(loaner=User.objects.filter(
            pnum='30002').get()).filter(document=self.av1).get()
        c4.booking_time = datetime.date(year=2018, month=2, day=17)
        c4.save()

        copies1 = \
            Copy.objects.filter(loaner=User.objects.filter(pnum='30001').get())
        print({copy.document: datetime.date.today() - copy.checked_due() for copy in
               copies1})

        copies2 = \
            Copy.objects.filter(loaner=User.objects.filter(pnum='30002').get())
        print({copy.document: datetime.date.today() - copy.checked_due() for copy in
               copies2})


class TestCase3(TestCase):

    def setUp(self):
        self.librarian = Librarian.objects.create_user(
            pnum='0000000000', password='kek1', user_type='lib',
            is_superuser=True, is_staff=True)

        authors = [Author.objects.create(name='Thomas H. Cormen'),
                   Author.objects.create(name='Charles E. Leiserson'),
                   Author.objects.create(name='Ronald L. Rivest'),
                   Author.objects.create(name='Clifford Stein')
                   ]
        self.d1 = Book.objects.create(
            title='Introduction to Algorithms',
            publisher='MIT press',
            year=datetime.date(2009, 10, 10),
            edition='Third edition',
            price=5000,
        )
        self.d1.authors.set(authors)

        authors = [Author.objects.create(name='Erich Gamma'),
                   Author.objects.create(name='Ralph Johnson'),
                   Author.objects.create(name='John Vlisidos'),
                   Author.objects.create(name='Richard Helm')
                   ]
        self.d2 = Book.objects.create(
            title='Design Patterns: Elements of '
            'Reusable Object-Oriented Software',
            publisher='Addison-Wesley Professional',
            year=datetime.date(2003, 10, 10),
            edition="First edition",
            price=1700,
            is_bestseller=True,
        )
        self.d2.authors.set(authors)

        author = [Author.objects.create(name='Tony Huare')]
        self.d3 = Book.objects.create(title='Null References: '
                                      'The Billion Dollar Mistake',
                                      publisher=' ',
                                      year=datetime.date(2003, 10, 10),
                                      edition=" ",
                                      price=700,
                                      )
        self.d3.authors.set(author)

        self.d1.add_copy(self.librarian, ammount=3)
        self.d2.add_copy(self.librarian, ammount=3)
        self.d3.add_copy(self.librarian, ammount=2)
        self.librarian.add_user(Type=Professor,
                                user_type='prof',
                                name='Sergey',
                                surname='Afonso',
                                address='Via Margutta, 3',
                                pnum='30001',
                                password='innopolis1')
        self.librarian.add_user(Type=Professor,
                                user_type='prof',
                                name='Nadia',
                                surname='Teixeira',
                                address='Via Sacra, 13',
                                pnum='30002',
                                password='innopolis1')
        self.librarian.add_user(Type=Professor,
                                user_type='prof',
                                name='Elvira',
                                surname='Espindola',
                                address='Via del Corso, 22',
                                pnum='30003',
                                password='innopolis1')
        self.librarian.add_user(Type=Student,
                                user_type='stu',
                                name='Andrey',
                                surname='Velo',
                                address='Avenida Mazatlan 250',
                                pnum='30004',
                                password='innopolis1')
        self.librarian.add_user(Type=VisitingProfessor,
                                user_type='vp',
                                name='Veronika',
                                surname='Rama',
                                address='Street Atocha,27',
                                pnum='30005',
                                password='innopolis1')

        self.p1 = User.objects.filter(pnum="30001").get()
        self.p2 = User.objects.filter(pnum="30002").get()
        self.p3 = User.objects.filter(pnum="30003").get()
        self.s = User.objects.filter(pnum="30004").get()
        self.v = User.objects.filter(pnum="30005").get()

    def test0(self):
        print(User.objects.all())

    def get_info(self, user):
        copies = Copy.objects.filter(loaner=user)
        docs = {copy.document: [copy.get_overdue(), copy.get_fine(),
                                copy.checked_due()] for copy in copies}
        return{
            # 'name': user.get_full_name(),
            # 'adress': user.address,
            'pnum': user.pnum,
            # 'card_id': user.pnum,
            'type': user.user_type,
            'docs': docs,
        }

    def test1(self):
        self.d1.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()
        self.d2.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()
        print(self.get_info(self.p1))

    def test2(self):
        self.d1.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()
        self.d2.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()

        self.d1.check_out(self.s)
        c1 = Copy.objects.filter(loaner=self.s, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()
        self.d2.check_out(self.s)
        c1 = Copy.objects.filter(loaner=self.s, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()

        self.d1.check_out(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()
        self.d2.check_out(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=7)
        c1.save()

        print(self.get_info(self.p1))
        print(self.get_info(self.s))
        print(self.get_info(self.v))

    def test3(self):
        self.d1.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d2.check_out(self.s)
        c1 = Copy.objects.filter(loaner=self.s, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d2.check_out(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d1.renew_doc(self.p1)
        self.d2.renew_doc(self.s)
        self.d2.renew_doc(self.v)

        print(self.get_info(self.p1))
        print(self.get_info(self.s))
        print(self.get_info(self.v))

    def test4(self):
        self.d1.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d2.check_out(self.s)
        c1 = Copy.objects.filter(loaner=self.s, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d2.check_out(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d2).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d2.outstanding(self.librarian)

        self.d1.renew_doc(self.p1)
        self.d2.renew_doc(self.s)
        self.d2.renew_doc(self.v)

        print(self.get_info(self.p1))
        print(self.get_info(self.s))
        print(self.get_info(self.v))

    def test5(self):
        self.d3.check_out(self.p1)
        self.d3.check_out(self.s)
        self.d3.check_out(self.v)
        print(self.d3.get_waiting_list())

    def test6(self):
        self.d3.check_out(self.p1)
        self.d3.check_out(self.p2)
        self.d3.check_out(self.s)
        self.d3.check_out(self.v)
        self.d3.check_out(self.p3)
        print(self.d3.get_waiting_list())

    def test7(self):
        self.test6()
        self.d3.outstanding(self.librarian)
        print(self.p1.messages.all())
        print(self.p2.messages.all())
        print(self.s.messages.all())
        print(self.v.messages.all())
        print(self.p3.messages.all())
        self.assertEqual(len(self.d3.get_waiting_list()), 0)

    def test8(self):
        self.test6()
        self.d3.return_doc(self.p2)
        print(self.s.messages.all())
        print(self.get_info(self.p2))
        print(self.d3.get_waiting_list())

    def test9(self):
        self.test6()
        self.d3.renew_doc(self.p1)
        print(self.get_info(self.p1))
        print(self.d3.get_waiting_list())

    def test10(self):
        self.d1.check_out(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=26)
        c1.save()
        self.d1.renew_doc(self.p1)
        c1 = Copy.objects.filter(loaner=self.p1, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        self.d1.check_out(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=26)
        c1.save()
        self.d1.renew_doc(self.v)
        c1 = Copy.objects.filter(loaner=self.v, document=self.d1).get()
        c1.booking_time = datetime.date(year=2018, month=3, day=29)
        c1.save()

        print(self.get_info(self.p1))
        print(self.get_info(self.v))


class TestCase4(TestCase):

    def setUp(self):
        self.admin = Admin.objects.create_user(
            pnum='00000000000', password='innopoles1', name='Admin')

    def system_info(self, user):
        docs = ['{0} , copies:{1}']

    def test1(self):
        try:
            Admin.objects.create_user(
                pnum='00000000001', password='innopoles1', name='Admin2')
        except Exception as e:
            print(e)

    def test2(self):
        self.admin.add_user(
            Librarian, pnum='0000000001', password='innopeles1', name='L1',
            privilege=1)
        self.admin.add_user(
            Librarian, pnum='0000000002', password='innopelez1', name='L2',
            privilege=2)
        self.admin.add_user(
            Librarian, pnum='0000000003', password='innopeliz', name='L3',
            privilege=3)
        self.l1 = Librarian.objects.filter(pnum='0000000001').get()
        self.l2 = Librarian.objects.filter(pnum='0000000002').get()
        self.l3 = Librarian.objects.filter(pnum='0000000003').get()

    def test3(self):
        self.test2()
        try:
            Book.add_doc(
                user=self.l1,
                title='Introduction to Algorithms',
                publisher='MIT press',
                year=datetime.date(2009, 10, 10),
                edition='Third edition',
                price=5000,
            )
            keywords = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Data Structures'),
                Keyword.objects.create(word='Complexity'),
                Keyword.objects.create(word='Computational Theory'),
            ]
            authors = [
                Author.objects.create(name='Thomas H. Cormen'),
                Author.objects.create(name='Charles E. Leiserson'),
                Author.objects.create(name='Ronald L. Rivest'),
                Author.objects.create(name='Clifford Stein'),
            ]
        except ValidationError as e:
            print(e)
        else:
            print('OK')
        try:
            Book.add_doc(
                user=self.l1,
                title='Algorithms + Data Structures = Programs',
                publisher='Prentice Hall PTR',
                year=datetime.date(1978, 10, 10),
                edition='First edition',
                price=5000,
            )
            authors = [
                Author.objects.create(name='Niklaus Wirth'),
            ]
            keywords = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Data Structures'),
                Keyword.objects.create(word='Search Algoriths'),
                Keyword.objects.create(word='Pascal'),
            ]
        except ValidationError as e:
            print(e)
        else:
            print('OK')
        try:
            Book.add_doc(
                user=self.l1,
                title='The Art of Computer Programming',
                publisher='Addison Wesley Longman Publishing Co., Inc.',
                year=datetime.date(1997, 10, 10),
                edition='Third edition',
                price=5000,
            )
            authors = [
                Author.objects.create(name='Niklaus Wirth'),
            ]
            keywords = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Combinational Algoriths'),
                Keyword.objects.create(word='Recursion'),
            ]
        except ValidationError as e:
            print(e)
        else:
            print('OK')
        print(Document.objects.all())

    def test4(self):
        self.test2()
        try:
            Book.add_doc(
                user=self.l2,
                title='Introduction to Algorithms',
                publisher='MIT press',
                year=datetime.date(2009, 10, 10),
                edition='Third edition',
                price=5000,
            )
            keywords1 = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Data Structures'),
                Keyword.objects.create(word='Complexity'),
                Keyword.objects.create(word='Computational Theory'),
            ]
            authors1 = [
                Author.objects.create(name='Thomas H. Cormen'),
                Author.objects.create(name='Charles E. Leiserson'),
                Author.objects.create(name='Ronald L. Rivest'),
                Author.objects.create(name='Clifford Stein'),
            ]
            Book.objects.all()[0].add_copy(user=self.l2, ammount=3)
        except ValidationError as e:
            print(e)
        try:
            Book.add_doc(
                user=self.l2,
                title='Algorithms + Data Structures = Programs',
                publisher='Prentice Hall PTR',
                year=datetime.date(1978, 10, 10),
                edition='First edition',
                price=5000,
            )
            authors2 = [
                Author.objects.create(name='Niklaus Wirth'),
            ]
            keywords2 = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Data Structures'),
                Keyword.objects.create(word='Search Algoriths'),
                Keyword.objects.create(word='Pascal'),
            ]
            Book.objects.all()[1].add_copy(user=self.l2, ammount=3)
        except ValidationError as e:
            print(e)
        try:
            Book.add_doc(
                user=self.l2,
                title='The Art of Computer Programming',
                publisher='Addison Wesley Longman Publishing Co., Inc.',
                year=datetime.date(1997, 10, 10),
                edition='Third edition',
                price=5000,
            )
            authors3 = [
                Author.objects.create(name='Niklaus Wirth'),
            ]
            keywords3 = [
                Keyword.objects.create(word='Algorithms'),
                Keyword.objects.create(word='Combinational Algoriths'),
                Keyword.objects.create(word='Recursion'),
            ]
            Book.objects.all()[2].add_copy(user=self.l2, ammount=3)
        except ValidationError as e:
            print(e)
        self.d1, self.d2, self.d3 = Book.objects.all()
        self.d1.authors.set(authors1)
        self.d1.keywords.set(keywords1)
        self.d2.authors.set(authors2)
        self.d2.keywords.set(keywords2)
        self.d3.authors.set(authors3)
        self.d3.keywords.set(keywords3)
        # user addition
        try:
            self.l2.add_user(
                Professor,
                name='Sergey Afonso',
                pnum='30001',
                address='Via Margutta, 3',
                password='innolelez',
            )
        except ValidationError as e:
            print(e)
        try:
            self.l2.add_user(
                Professor,
                name='Nadia Teixeira',
                pnum='30002',
                address='Via Sacra, 13',
                password='innovatzii',
            )
        except ValidationError as e:
            print(e)
        try:
            self.l2.add_user(
                Professor,
                name='Elvira Espindola',
                pnum='30003',
                address='Via Del Corso, 22',
                password='innoshkoderi',
            )
        except ValidationError as e:
            print(e)
        try:
            self.l2.add_user(
                Student,
                name='Andrey Velo',
                pnum='30004',
                address='Via Del Corso, 22',
                password='innocheburek',
            )
        except ValidationError as e:
            print(e)
        try:
            self.l2.add_user(
                VisitingProfessor,
                name='Veronika Rama',
                pnum='30005',
                address='Stret Atocha, 27',
                password='siloponni',
            )
        except ValidationError as e:
            print(e)
        self.p1, self.p2, self.p3, self.s, self.v = Patron.objects.all()
        print(check_system(self.l2))


    def test5(self):
        self.test4()
        self.d3.remove_copy(user=self.l3, ammount=1)
        print(self.d3.number_of_copies)

    def test6(self):
        self.test4()
        self.d3.check_out(self.p1)
        self.d3.check_out(self.p2)
        self.d3.check_out(self.s)
        self.d3.check_out(self.v)
        self.d3.check_out(self.p3)
        try:
            self.d3.outstanding(user=self.l1)
        except ValidationError as e:
            print(e)

    def test7(self):
        self.test4()
        self.d3.check_out(self.p1)
        self.d3.check_out(self.p2)
        self.d3.check_out(self.s)
        self.d3.check_out(self.v)
        self.d3.check_out(self.p3)
        try:
            self.d3.outstanding(user=self.l3)
        except ValidationError as e:
            print(e)
        print('Waiting list of "{1}" :{0}'.format(self.d3.get_waiting_list(),
                                                  self.d3))
        print(self.s.messages.all())
        print(self.p1.messages.all())
        print(self.p2.messages.all())
        print(self.v.messages.all())
        print(self.p3.messages.all())

    def test8(self):
        self.test6()
        for i in self.admin.check_log():
            print(i)

    def test9(self):
        self.test7()
        for i in self.admin.check_log():
            print(i)

    def test10(self):
        self.test7()
        docs = search(user=self.v, title='Introduction to Algorithms')
        print('Found docs:')
        for i in docs:
            print(i)

    def test11(self):
        self.test4()
       # os.system('cls' if os.name == 'nt' else 'clear')
        docs = search(user=self.v, title='Algorithms')
        print('Found docs:')
        for i in docs:
            print(i)

    def test12(self):
        self.test7()
        docs = search(user=self.v, keyword='Algorithms')
        print('Found docs:')
        for i in docs:
            print(i)

    def test13(self):
        self.test4()
        docs = list(set(search(user=self.v,
                               title='Algorithms')).intersection(set(search(user=self.v,
                                                                            title='Programming'))))
        print('Found docs:')
        for i in docs:
            print(i)

    def test14(self):
        self.test4()
        docs = list(set(search(user=self.v,
                               title='Algorithms')).union(set(search(user=self.v,title='Programming'))))
        print('Found docs:')
        for i in docs:
            print(i)
