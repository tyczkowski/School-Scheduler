from django.test import TestCase
from TAServer.models import Section, Course, Staff as User
from Managers.sectionManager import SectionManager as SM
from Managers.DjangoStorageManager import DjangoStorageManager as storage

class sectionTest(TestCase):

    def setUp(self):

        self.u1 = User.objects.create(username="Gumby", first_name="Gimpy", last_name="McGoo",
                 email="Gumby@gmail.com", password="123", role="instructor")
        self.u1.save()
        self.c1 = Course.objects.create(cnum="351", name="Data Structures and Algorithms",
                    description="N/A", dept="CS")
        self.c1.save()
        self.s1 = Section.objects.create(snum="401", stype="lecture", course=self.c1, room=395, instructor=self.u1,
                     days="W", time="12:30PM-1:30PM")
        self.s1.save()
        self.u2 = User.objects.create(username="Rock", first_name="Jayson", last_name="Rock",
                 email="jRock@gmail.com", password="123", role="instructor")
        self.u2.save()
        self.u3 = User.objects.create(username="Crunchy", first_name="Ron", last_name="Skimpy",
                 email="BubbaGump@gmail.com", password="shrimp", role="administrator")
        self.u3.save()
        temp = storage()
        self.sec = SM()

    def tearDown(self):
        pass

    # Test correct adding
    def test_add(self):
        newSec = {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 901, "instructor": "Gumby",
                  "days": "T", "time": "4:00PM-5:00PM"}
        self.assertTrue(self.sec.add(newSec), "New section was not added")

    # Test add when given various invalid field inputs
    def test_addInvalid(self):
        addDays = {"cnum": "351", "dept": "CS", "snum": "401", "days": "Wrong", "instructor": "Rock", "room": 400,
                  "time": "1:00PM-2:00PM", "snumNew": "402"}
        addIns = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Crunchy", "room": 400,
                  "time": "1:00PM-2:00PM", "snumNew": "402"}
        addRoom = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": "Wrong",
                  "time": "1:00PM-2:00PM", "snumNew": "402"}
        addTime = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                  "time": "Wrong", "snumNew": "402"}
        addsnum = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                  "time": "1:00PM-2:00PM", "snumNew": "Wrong"}
        self.assertFalse(self.sec.add(addDays), "Should return false due to invalid days input")
        self.assertFalse(self.sec.add(addIns), "Should return false due to invalid instructor")
        self.assertFalse(self.sec.add(addRoom), "Should return false due to invalid room number")
        self.assertFalse(self.sec.add(addTime), "Should return false due to invalid time")
        self.assertFalse(self.sec.add(addsnum), "Should return false due to invalid section number")

    # Test adding without requirements (cnum, dept, snum)
    def test_addNoInfo(self):
        secNocnum= {"snum": "401", "dept": "CS"}
        secNoSnum= {"cnum": "351", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.sec.add(secNocnum), "Should return false when no course number is specified")
        self.assertFalse(self.sec.add(secNoSnum), "Should return false when no section number is specified")
        self.assertFalse(self.sec.add(secNodept), "Should return false when no department is specified")

    # user does not exist and shouldn't be able to be added
    def test_userNone(self):
        secUserInv= {"snum": "801", "instructor": "Bubba", "cnum":"351", "dept":"CS"}
        self.assertFalse(self.sec.add(secUserInv), "User Bubba does not exist in the system")

    # test that adding fails when adding a new Section whose time and room conflict with another currently existing one
    def test_addRoomTimeConflict(self):
        secConflict= {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 395, "instructor": "Gumby",
                  "days": "W", "time": "12:30PM-1:00PM"}
        self.assertFalse(self.sec.add(secConflict), "Section added conflicts with already created section")

    # test "section view secNum" command output
    def test_view(self):
        toView= {"snum":"401", "cnum":"351", "dept":"CS"}
        self.assertEqual(self.sec.view(toView),
                         "Course: CS-351<br>Section: 401<br>Instructor: Gumby<br>Meeting time(s): W 12:30PM-1:30PM"
                         "<br>Room: 395")

    # Test to make sure a course without a section will not be found
    def test_viewNot(self):
        self.courseT = Course(cnum="337", name="Systems Programming",
                    description="N/A", dept="CS")
        self.courseT.save()
        toView = {"snum":"401", "dept": "CS", "cnum": "337"}
        self.assertEqual("Could not find CS-337-401", self.sec.view(toView))

    # Test view without enough information
    def test_viewNoInfo(self):
        secNocnum= {"snum": "401", "dept": "CS"}
        secNoSnum= {"cnum": "351", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertEqual(self.sec.view(secNocnum), "Could not complete viewing, course number is needed",
                         "Should not be able to view without course specified")
        self.assertEqual(self.sec.view(secNoSnum), "Could not complete viewing, section number is needed",
                         "Should not be able to view without section number specified")
        self.assertEqual(self.sec.view(secNodept), "Could not complete viewing, department is needed",
                         "Should not be able to view without department specified")

    def test_delete(self):
        toDel= {"snum": "401", "cnum": "351", "dept": "CS"}
        self.assertTrue(self.sec.delete(toDel), "Delete was not successful")

    # make sure required information is there to delete
    def test_delNoInfo(self):
        secNoSnum = {"cnum": "351", "dept": "CS"}
        secNocnum = {"snum": "401", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.sec.delete(secNocnum), "Should return false when no course number is specified")
        self.assertFalse(self.sec.delete(secNoSnum), "Should return false when no section number is specified")
        self.assertFalse(self.sec.delete(secNodept), "Should return false when no department is specified")

    def test_edit(self):
        toEdit= {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400, "time": "1:00PM-2:00PM"}
        self.assertTrue(self.sec.edit(toEdit), "Edit was not successful")

    # Test edit without enough info
    def test_editNoInfo(self):
        secNocnum= {"snum": "401", "dept": "CS"}
        secNoSnum= {"cnum": "351", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.sec.delete(secNocnum), "Should return false when no course number is specified")
        self.assertFalse(self.sec.delete(secNoSnum), "Should return false when no section number is specified")
        self.assertFalse(self.sec.delete(secNodept), "Should return false when no department is specified")

    # Test edit when given various invalid field inputs
    def test_editInvalid(self):
        editDays = {"cnum": "351", "dept": "CS", "snum": "401", "days": "Wrong", "instructor": "Rock", "room": 400,
                  "time": "1:00PM-2:00PM"}
        editIns = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Crunchy", "room": 400,
                  "time": "1:00PM-2:00PM"}
        editRoom = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": "Wrong",
                  "time": "1:00PM-2:00PM"}
        editTime = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                  "time": "Wrong"}
        self.assertFalse(self.sec.edit(editDays), "Should return false due to invalid days input")
        self.assertFalse(self.sec.edit(editIns), "Should return false due to invalid instructor")
        self.assertFalse(self.sec.edit(editRoom), "Should return false due to invalid room number")
        self.assertFalse(self.sec.edit(editTime), "Should return false due to invalid time")

    # Need to make sure that the "time" field accepts multiple ways of inputting (e.g "01:30 PM", "1:30 PM"
    def test_editTimes(self):
        timeOne = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                    "time": "01:30PM-02:30PM"}
        timeTwo = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                    "time": "3:30PM-4:30PM"}
        self.assertTrue(self.sec.edit(timeOne), "Editing time was not successful")
        self.assertTrue(self.sec.edit(timeTwo), "Editing time was not successful")

    # Test that if, upon editing, the if the new room and time conflict with a previously added section, it fails.
    def test_editRoomTimeConflict(self):
        newSec = {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 901, "instructor": "Gumby",
                  "days": "T", "time": "4:00PM-5:00PM"}
        self.sec.add(newSec)
        secConflict= {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 395, "instructor": "Gumby",
                  "days": "W", "time": "12:30PM-1:00PM"}
        self.assertFalse(self.sec.edit(secConflict), "Section added conflicts with already created section")