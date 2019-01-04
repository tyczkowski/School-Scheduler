import unittest

from Managers.JSONStorageManager import JSONStorageManager as StorageManager
from Managers.courseManager import CourseManager
from Managers.sectionManager import SectionManager
from TAServer.models import Staff as User


class sectionTest(unittest.TestCase):

    def setUp(self):
        self.course = CourseManager()
        self.course.add(dept="CS", cnum="251")
        self.db = StorageManager()
        Bob = User("Bob", "123", "Instructor")
        self.db.insert_user(Bob)
        Rob = User("Rob", "123")
        self.db.insert_user(Rob)
        Cobb = User("Randall Cobb", "123", "Instructor")
        self.db.insert_user(Cobb)
        self.course.add(dept="CS", cnum="351", instr="Bob", section="401")
        self.course.add(dept="CS", cnum="337")
        self.sec = SectionManager()

    def tearDown(self):
        del self.course
        del self.sec
        del self.db

    def test_add(self):
        self.assertEqual(self.sec.add("CS", "251", "401"), "Section Added: CS-251-401")
        self.assertEqual(self.sec.add("CS", "251", "401", "Bob"), "Section Added: CS-251-401 instructor: Bob")

    def test_addNoInfo(self):
        self.assertEqual("Could not complete addition, section number is needed",
                         self.sec.add(dept="CS", cnum="251"))
        self.assertEqual("Could not complete addition, section number is needed",
                         self.sec.add(dept="CS", cnum="251", ins="Bob"))
        self.assertEqual("Could not complete addition, course number is needed",
                         self.sec.add(dept="CS", snum="401", ins="Bob"))
        self.assertEqual("Could not complete addition, department is needed",
                         self.sec.add(cnum="251", snum="401", ins="Bob"))

    # user does not exist and shouldn't be able to be added
    def test_userNone(self):
        self.assertEqual("Nobody does not exist in the system",
                         self.sec.add(dept="CS", cnum="251", snum="401", ins="Nobody"))

    def test_notQualified(self):
        self.assertEqual("User can't instruct the course", self.sec.add(dept="CS", cnum="337", snum="401", ins="Rob"))

    # test "section view secNum" command output
    def test_view(self):
        self.assertEqual(self.sec.view(dept="CS", cnum="351", snum="401"),
                         "Course: CS-351\nSection: 401\nInstructor: Bob")

    # Test to make sure a course without a section will not be found
    def test_viewNot(self):
        self.assertEqual("Could not find CS-337-401", self.sec.view(dept="CS", cnum="337", snum="401"))

    def test_viewNoInfo(self):
        self.assertEqual("Could not complete view, section number is needed",
                         self.sec.view(dept="CS", cnum="251"))
        self.assertEqual("Could not complete view, section number is needed",
                         self.sec.view(dept="CS", cnum="251", ins="Bob"))
        self.assertEqual("Could not complete view, course number is needed",
                         self.sec.view(dept="CS", snum="401", ins="Bob"))
        self.assertEqual("Could not complete view, department is needed",
                         self.sec.view(cnum="251", snum="401", ins="Bob"))
