from Managers.DjangoStorageManager import DjangoStorageManager
from TAServer.models import Staff as User, Course, Section
from django.test import TestCase
import unittest


class DjangoStorageManagerTests(TestCase):

    # setUp Calls setup function from db. This makes sense as all databases have a hardcoded supervisor to start with,
    # and we test if setup does what it is supposed to later.
    def setUp(self):
        DjangoStorageManager.set_up(overwrite=False)

    # This test just makes sure that after a set_up call (we call this during def setUp in this class) there is a
    # starter supervisor
    def test_set_up(self):
        self.assertEqual(User.objects.all().count(), 1, "After setup, must contain one user!")
        self.assertEqual(Section.objects.all().count(), 0)
        self.assertEqual(Course.objects.all().count(), 0)

        self.assertEqual(User.objects.filter(username="supervisor").count(), 1)
        u = User.objects.get(username="supervisor")
        self.assertIsNotNone(u)
        self.assertEqual(u.password, "123")
        self.assertEqual(u.role, dict(User.ROLES)["S"])

        # Testing database flushing (Overwrite = True
        newuser = User(username= "test", password = "password", role = "")
        newuser.save()
        newcourse = Course(dept="CS", cnum="351")
        newcourse.save()
        newsection = Section(snum = "801", course = newcourse)
        newsection.save()

        u = User.objects.get(username = "test")
        c = Course.objects.get(dept="CS", cnum="351")
        s = Section.objects.get(snum="801", course__dept= "CS", course__cnum="351")
        self.assertIsNotNone(u)
        self.assertIsNotNone(c)
        self.assertIsNotNone(s)

        # Should rebuild database, with none of the following models we had created:
        DjangoStorageManager.set_up(overwrite=True)
        self.assertEqual(User.objects.all().count(), 1, "After rebuild (overwrite), must contain one user!")
        self.assertEqual(Section.objects.all().count(), 0)
        self.assertEqual(Course.objects.all().count(), 0)

    # NOTE: FOR ALL OTHER TESTS WE ASSUME SETUP WORKS CORRECTLY AND ONLY ONE SUPERUSER IS IN THE DATABASE

    # Testing insert_course
    def test_insert_course(self):
        c = Course(dept = "CS", cnum = "351")
        self.assertFalse(DjangoStorageManager.insert_course(c), "Should return false, not overwriting!")
        retval = Course.objects.get(dept="CS", cnum="351")
        self.assertIsNotNone(retval)
        c.name = "Data Structures and Algorithms"
        self.assertTrue(DjangoStorageManager.insert_course(c), "Should return true, overwriting!")
        retval = Course.objects.get(dept="CS", cnum="351")
        self.assertIsNotNone(retval)
        self.assertEqual(Course.objects.all().count(), 1, "Should only be 1 course in Courses during this test!")
        self.assertEqual(retval.name, "Data Structures and Algorithms", "Insert didn't properly update the db!")

    # Testing insert_section
    def test_insert_section(self):
        c = Course(dept="CS", cnum="351")
        c.save()
        s = Section(snum="801", course=c)
        self.assertFalse(DjangoStorageManager.insert_section(s), "Should return false, not overwriting!")
        retval = Section.objects.get(snum="801", course__dept="CS", course__cnum="351")
        self.assertIsNotNone(retval)
        s.time = "11:00AM"
        self.assertTrue(DjangoStorageManager.insert_section(s), "Should return true, overwriting!")
        retval = Section.objects.get(snum="801", course__dept="CS", course__cnum="351")
        self.assertIsNotNone(retval)
        self.assertEqual(len(Section.objects.all()), 1, "Should only be 1 section in Sections during this test!")
        self.assertEqual(retval.time, "11:00AM", "Insert didn't properly update the db!")

    # Testing insert_user
    def test_insert_user(self):
        u = User(username="Rock", password="123")
        self.assertFalse(DjangoStorageManager.insert_user(u), "Should return false, not overwriting!")
        retval = User.objects.get(username="Rock")
        self.assertIsNotNone(retval)
        u.password = "password"
        u.role=dict(User.ROLES)["I"]
        self.assertTrue(DjangoStorageManager.insert_user(u), "Should return true, overwriting!")
        retval = User.objects.get(username="Rock")
        self.assertIsNotNone(retval)
        self.assertEqual(User.objects.all().count(), 2, "Should only be 2 users in Users during this test!")
        self.assertEqual(retval.password, "password", "Insert didn't properly update the db!")
        self.assertEqual(retval.role, dict(User.ROLES)["I"], "Should have updated roles!")

    # Testing get_course
    def test_get_course(self):
        c = Course(dept="CS", cnum="351", name="Data Structures and Algorithms")
        c.save()
        retval = DjangoStorageManager.get_course(dept="CS", cnum="351")
        self.assertIsNotNone(retval)
        self.assertIsInstance(retval, Course)
        self.assertEqual(retval.name, "Data Structures and Algorithms")

    # Testing get_courses_by (filter version for searches)
    def test_get_courses_by(self):
        c1 = Course(dept="CS", cnum="351")
        c2 = Course(dept="CS", cnum="240")
        c3 = Course(dept="MATH", cnum="240")
        c1.save()
        c2.save()
        c3.save()

        # Testing getting course by providing dept and cnum (should be unique - 1 course!)
        retval = DjangoStorageManager.get_courses_by(dept="MATH", cnum="240")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 1)
        self.assertTrue(retval.__contains__(c3))

        # Testing getting course by providing dept
        retval = DjangoStorageManager.get_courses_by(dept="CS")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(c1))
        self.assertTrue(retval.__contains__(c2))

        # Testing getting course by providing cnum
        retval = DjangoStorageManager.get_courses_by(cnum="240")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(c2))
        self.assertTrue(retval.__contains__(c3))

        # Testing getting course by providing nothing (all)
        retval = DjangoStorageManager.get_courses_by()
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 3)
        self.assertTrue(retval.__contains__(c1))
        self.assertTrue(retval.__contains__(c2))
        self.assertTrue(retval.__contains__(c3))

    # Testing get_user
    def test_get_user(self):
        u = User(username="Rock", password="123", role=dict(User.ROLES)["I"])
        u.save()
        retval = DjangoStorageManager.get_user("Rock")
        self.assertIsNotNone(retval)
        self.assertIsInstance(retval, User)
        self.assertEqual(retval.password, "123")
        self.assertEqual(retval.role, dict(User.ROLES)["I"])

    # Testing get_users_by (Filter version for searches)
    def test_get_users_by(self):
        u1 = User(username="Rock", password="123", role=dict(User.ROLES)["I"])
        u2 = User(username="Boyland", password="Andrew", role=dict(User.ROLES)["I"])
        u1.save()
        u2.save()

        # Testing getting user by providing username(should be unique - 1 user!)
        retval = DjangoStorageManager.get_users_by(username="Rock")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 1)
        self.assertTrue(retval.__contains__(u1))

        # Testing getting user by providing role
        retval = DjangoStorageManager.get_users_by(role="Instructor") # dict(User.ROLES)["I"] -> Instructor
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(u1))
        self.assertTrue(retval.__contains__(u2))

        # Testing getting course by providing nothing (all users (sup included))
        retval = DjangoStorageManager.get_users_by()
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 3)
        self.assertTrue(retval.__contains__(u1))
        self.assertTrue(retval.__contains__(u2))

    # Testing get_section
    def test_get_section(self):
        c = Course(dept="CS", cnum="351", name="Data Structures and Algorithms")
        c.save()
        s = Section(snum="801", course=c, time="11:00AM")
        s.save()
        retval = DjangoStorageManager.get_section(snum="801",dept="CS", cnum="351")
        self.assertIsNotNone(retval)
        self.assertIsInstance(retval, Section)
        self.assertEqual(retval.time, "11:00AM")
        self.assertEqual(retval.course.cnum, "351")
        self.assertEqual(retval.course.dept, "CS")

    # Testing get_sections_by (filter version for searches)
    def test_get_sections_by(self):
        c1 = Course(dept="CS", cnum="351")
        c2 = Course(dept="CS", cnum="337")
        c1.save()
        c2.save()

        s1 = Section(snum="801", course=c1)
        s2 = Section(snum="801", course=c2)
        s3 = Section(snum ="802", course=c1)
        s1.save()
        s2.save()
        s3.save()

        # Testing getting sections by providing snum, dept, and cnum (should be unique - 1 section!)
        retval = DjangoStorageManager.get_sections_by(dept="CS", cnum="351", snum="801")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 1)
        self.assertTrue(retval.__contains__(s1))

        # Testing getting sections by providing dept
        retval = DjangoStorageManager.get_sections_by(dept="CS")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 3)
        self.assertTrue(retval.__contains__(s1))
        self.assertTrue(retval.__contains__(s2))
        self.assertTrue(retval.__contains__(s3))

        # Testing getting sections by providing cnum
        retval = DjangoStorageManager.get_sections_by(cnum="351")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(s1))
        self.assertTrue(retval.__contains__(s3))

        # Testing getting section by providing dept and cnum
        retval = DjangoStorageManager.get_sections_by(dept="CS", cnum="351")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(s1))
        self.assertTrue(retval.__contains__(s3))

        # Testing getting sections by providing dept and snum
        retval = DjangoStorageManager.get_sections_by(dept="CS", snum="801")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 2)
        self.assertTrue(retval.__contains__(s1))
        self.assertTrue(retval.__contains__(s2))

        # Testing getting sections by providing cnum and snum
        retval = DjangoStorageManager.get_sections_by(cnum="351", snum="801")
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 1)
        self.assertTrue(retval.__contains__(s1))

        # Testing getting sections by providing nothing (all)
        retval = DjangoStorageManager.get_sections_by()
        self.assertIsInstance(retval, list)
        self.assertEqual(len(retval), 3)
        self.assertTrue(retval.__contains__(s1))
        self.assertTrue(retval.__contains__(s2))
        self.assertTrue(retval.__contains__(s3))

    def test_delete(self):
        c = Course(dept="CS", cnum="351")
        s = Section(snum="801", course=c)
        u = User(username="Rock", password="123")

        # None of these objects are in the database, so nothing should be deleted
        self.assertFalse(DjangoStorageManager.delete(c))
        self.assertFalse(DjangoStorageManager.delete(s))
        self.assertFalse(DjangoStorageManager.delete(u))

        c.save()
        s.save()
        u.save()
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(Section.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 2)

        # Deleting objects here
        self.assertTrue(DjangoStorageManager.delete(s))
        self.assertTrue(DjangoStorageManager.delete(c))
        self.assertTrue(DjangoStorageManager.delete(u))
        self.assertEqual(Course.objects.all().count(), 0)
        self.assertEqual(Section.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 1)

        c = Course(dept="CS", cnum="351")
        s = Section(snum="801", course=c)
        u = User(username="Rock", password="123")

        c.save()
        s.save()
        u.save()

        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(Section.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 2)

        # Testing course -> section cascade delete
        # self.assertTrue(DjangoStorageManager.delete(c))
        # self.assertEqual(Course.objects.all().count(), 0)
        # self.assertEqual(Section.objects.all().count(), 0)
        # self.assertEqual(User.objects.all().count(), 2)
