from django.test import TestCase, Client
from django.urls import reverse
from TAServer.models import Staff, Course, Section
from Managers.userManager import UserManager as UM
from Managers.courseManager import CourseManager as CM
from Managers.sectionManager import SectionManager as SM
from Managers.DjangoStorageManager import DjangoStorageManager as ds
from TAServer.views import SectionViews as SV


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        adminUser = {"username":"Admin", "password": "Admin103", "role" :"Administrator"}
        self.storage = ds()
        self.user = UM(self.storage)
        self.user.add(adminUser)
        pass

    def tearDown(self):
        pass

    def test_urls(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/FAQ/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/courses/view')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/courses/add')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/sections/view')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/sections/add')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/user/view/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/user/add/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_Again(self):
        response = self.client.post(reverse('login'), data={'username': 'Admin', 'password': 'Admin103'}, follow=True)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'Admin')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Successful login should redirect to home page
        self.assertRedirects(response, '/home/')

        self.assertTrue(Staff.is_authenticated)
        self.client.logout()

    def test_user_add_success(self):
        self.client.post(reverse('login'), data={'username': 'Admin', 'password': 'Admin103'}, follow=True)

        response = self.client.post(reverse('User Add'), data={'username': 'John', 'password': '123', 'role': 'TA', 'email':'spazcat@aol.com'},
                                    follow=True)

        self.assertEqual(response.status_code, 200)

        person = self.storage.get_user('John')

        self.assertTrue(person.role, 'TA')
        self.assertEqual(person.email, 'spazcat@aol.com')

    def test_section_add_success(self):
        TAuser = {"username": "Tanawat", "password": "TA103", "role": "TA"}
        self.user.add(TAuser)
        user = self.storage.get_user('Tanawat')
        self.assertEqual(user.role, 'TA')

        self.client.post(reverse('login'), data={'username': 'Admin', 'password': 'Admin103'}, follow=True)

        response = self.client.post(reverse('Course Add'), data={'name': 'Cream', 'dept': 'CS', 'cnum': '400'}, follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('Section Add'), data={'stype': 'Lab', 'snum': '400', 'dept':'CS', 'cnum':'400',
                                                                  'room':'1', 'instructor':'Tanawat', 'days':'MWF', 'time':'12:30PM-1:30PM'}, follow=True)

        self.assertEqual(response.status_code, 200)

        sec = self.storage.get_section(snum='400', dept='CS', cnum='400')

        self.assertEqual(sec.snum, '400')
        self.assertEqual(sec.stype, 'Lab')
        self.assertEqual(sec.course.dept, 'CS')
        self.assertEqual(sec.course.cnum, '400')
        self.assertEqual(sec.room, 1)
        self.assertEqual(sec.days, 'MWF')
        self.assertEqual(sec.time, '12:30PM-1:30PM')

    def test_section_user_combined(self):
        self.client.post(reverse('login'), data={'username': 'Admin', 'password': 'Admin103'}, follow=True)

        response = self.client.post(reverse('User Add'), data={'username': 'John', 'password': '123', 'role': 'TA', 'email':'spazcat@aol.com'},
                                    follow=True)

        self.assertEqual(response.status_code, 200)

        person = self.storage.get_user('John')

        self.assertTrue(person.role, 'TA')
        self.assertEqual(person.email, 'spazcat@aol.com')

        response = self.client.post(reverse('Course Add'), data={'name': 'Cream', 'dept': 'CS', 'cnum': '400'}, follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('Section Add'), data={'stype': 'Lab', 'snum': '400', 'dept':'CS', 'cnum':'400',
                                                                  'room':'1', 'instructor':'John', 'days':'MWF', 'time':'12:30PM-1:30PM'}, follow=True)

        self.assertEqual(response.status_code, 200)

        sec = self.storage.get_section(snum='400', dept='CS', cnum='400')

        self.assertEqual(sec.snum, '400')
        self.assertEqual(sec.stype, 'Lab')
        self.assertEqual(sec.course.dept, 'CS')
        self.assertEqual(sec.course.cnum, '400')
        self.assertEqual(sec.room, 1)
        self.assertEqual(sec.days, 'MWF')
        self.assertEqual(sec.time, '12:30PM-1:30PM')

    def test_add_course_success(self):
        self.client.post(reverse('login'), data={'username': 'Admin', 'password': 'Admin103'}, follow=True)

        response = self.client.post(reverse('User Add'), data={'username': 'John', 'password': '123', 'role': 'TA', 'email':'spazcat@aol.com'},
                                    follow=True)

        self.assertEqual(response.status_code, 200)

        person = self.storage.get_user('John')

        self.assertTrue(person.role, 'TA')
        self.assertEqual(person.email, 'spazcat@aol.com')

        response = self.client.post(reverse('Course Add'), data={'name': 'Cream', 'dept': 'CS', 'cnum': '400'}, follow=True)

        self.assertEqual(response.status_code, 200)

        c = self.storage.get_course(dept='CS', cnum="400")

        self.assertEqual(c.name, 'Cream')