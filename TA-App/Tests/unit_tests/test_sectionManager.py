from django.test import TestCase
from TAServer.models import Section, Course, Staff as User
from Managers.sectionManager import SectionManager as SM
from Managers.DjangoStorageManager import DjangoStorageManager
from Managers.courseManager import CourseManager as CM
from Managers.userManager import UserManager as UM

class sectionTest(TestCase):

    def setUp(self):
        self.storage = DjangoStorageManager
        self.section_manager = SM(self.storage)
        self.course_manager = CM(self.storage)
        self.user_manager = UM(self.storage)

    def tearDown(self):
        pass

    # Test correct adding (basic), with courses
    def test_add(self):
        fields = {"dept": "CS",
                  "cnum": "351",
                  "snum": "401"}

        self.assertEqual(len(self.course_manager.view({})), 0, "Should have no courses to start")
        self.assertFalse(self.section_manager.add(fields)[0], "Can't add when there is no course!")
        self.course_manager.add({"dept":"CS", "cnum": "351"})
        self.assertTrue(self.section_manager.add(fields)[0])
        self.assertFalse(self.section_manager.add(fields)[0], "Shouldn't be able to add anymore")

    # Test correct adding and editing (assigning)
    def test_add_and_assign_ta(self):
        sectionFields = {"dept": "CS",
                         "cnum": "351",
                         "snum": "801"}

        userFields = {"username": "teach",
                      "password": "123",
                      "role": dict(User.ROLES)['T']}

        self.user_manager.add(userFields)
        self.course_manager.add({"dept":"CS", "cnum":"351"})
        self.assertTrue(self.section_manager.add(sectionFields)[0])

        # Course integration
        retVal = self.storage.get_course(dept="CS", cnum="351")
        self.assertEqual(retVal.sections.first().snum, "801", "course should have a working 'sections' field!")

        # Assigning TA
        sectionFields["instructor"] = "john"
        self.assertFalse(self.section_manager.edit(sectionFields)[0], "john doesn't exist!")
        sectionFields["instructor"] = "teach"
        self.assertFalse(self.section_manager.edit(sectionFields)[0], "shouldn't be able to edit, stype not lab when teach is TA")
        sectionFields["stype"] = dict(Section.SEC_TYPE)["lab"]
        self.assertTrue(self.section_manager.edit(sectionFields)[0], "valid assignment")

        # User integration, should now have courses and sections assigned
        retVal = self.storage.get_user("teach")
        self.assertEqual(retVal.sections.first().snum, "801", "user should have a working 'sections' field")
        self.assertEqual(retVal.courses.first().cnum, "351", "user should have a working 'courses' field")

    # The SuperTest Basically
    #def test_assign_instructor_TAs_and_check_all_thorough(self):
     #   pass

    # Test adding without requirements (cnum, dept, snum)
    def test_add_wrong_fields(self):
        secNocnum= {"snum": "401", "dept": "CS"}
        secNoSnum= {"cnum": "351", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.section_manager.add(secNocnum)[0], "Should return false when no course number is specified")
        self.assertFalse(self.section_manager.add(secNoSnum)[0], "Should return false when no section number is specified")
        self.assertFalse(self.section_manager.add(secNodept)[0], "Should return false when no department is specified")

    # user does not exist and shouldn't be able to be added
    def test_userNone(self):
        secUserInv= {"snum": "801", "instructor": "Bubba", "cnum":"351", "dept":"CS"}
        self.assertFalse(self.section_manager.add(secUserInv)[0], "User Bubba does not exist in the system")

    # test that adding fails when adding a new Section whose time and room conflict with another currently existing one
    def test_addRoomTimeConflict(self):
        secConflict= {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 395, "instructor": "Gumby",
                  "days": "W", "time": "12:30PM-1:00PM"}
        self.assertFalse(self.section_manager.add(secConflict)[0], "Section added conflicts with already created section")

    # test "section view secNum" command output
    def test_view(self):
        sectionFields = {"dept": "CS",
                         "cnum": "351",
                         "snum": "401",
                         "stype": "Lecture",
                         "instructor": "Rock"}

        userFields = {"username": "Rock",
                      "password": "123",
                      "role": dict(User.ROLES)['I']}
        self.course_manager.add({"dept":"CS", "cnum":"351"})
        self.user_manager.add(userFields)
        self.section_manager.add(sectionFields)

        retSection = self.section_manager.view({"dept":"CS", "cnum":"351", "snum":"401"})[0]
        self.assertEqual(retSection["dept"], "CS")
        self.assertEqual(retSection["cnum"], "351")
        self.assertEqual(retSection["snum"], "401")
        self.assertEqual(retSection["stype"], "Lecture")
        self.assertEqual(retSection["instructor"], "Rock")
        self.assertEqual(retSection["course"]["cnum"], "351")
        # Important!
        self.assertEqual(retSection["course"]["sections"], ["nonrecursive"])

    # Test to make sure 3 seperate sections can be viewed. Big test
    def test_view_all_comprehensive_integrated(self):
        self.course_manager.add({"dept":"CS", "cnum":"351"})
        self.course_manager.add({"dept":"CS", "cnum":"337"})
        sectionFields1 = {"dept":"CS",
                          "cnum":"351",
                          "snum":"401",
                          "stype":"Lecture",
                          "instructor":"Boyland"}

        sectionFields2 = {"dept":"CS",
                          "cnum":"351",
                          "snum":"801",
                          "stype":"Lab",
                          "instructor":"Tanawat"}

        sectionFields3 = {"dept":"CS",
                          "cnum":"337",
                          "snum":"401",
                          "stype":"Lecture",
                          "instructor":"Sorenson"}

        self.user_manager.add({"username":"Boyland", "role":dict(User.ROLES)["I"]})
        self.user_manager.add({"username": "Tanawat", "role": dict(User.ROLES)["T"]})
        self.user_manager.add({"username": "Sorenson", "role": dict(User.ROLES)["I"]})

        self.section_manager.add(sectionFields1)
        self.section_manager.add(sectionFields2)
        self.section_manager.add(sectionFields3)

        retList = self.section_manager.view({})
        self.assertEqual(len(retList), 3)
        retFields1 = retList[0]
        retFields2 = retList[1]
        retFields3 = retList[2]

        # Ordered properly?
        self.assertEqual(retFields1["cnum"], "337")
        self.assertEqual(retFields2["cnum"], "351")
        self.assertEqual(retFields2["snum"], "401")
        self.assertEqual(retFields3["cnum"], "351")
        self.assertEqual(retFields3["snum"], "801")

    def test_delete(self):
        toDel= {"snum": "401", "cnum": "351", "dept": "CS"}
        self.course_manager.add({"dept":"CS", "cnum":"351"})
        self.section_manager.add(toDel)
        self.assertTrue(self.section_manager.delete(toDel)[0], "Delete was not successful")

    def test_delete_doesntexist(self):
        toDel = {"snum": "401", "cnum": "351", "dept": "CS"}
        self.assertFalse(self.section_manager.delete(toDel)[0], "Delete shouldn't be successful")

    # make sure required information is there to delete
    def test_delNoInfo(self):
        secNoSnum = {"cnum": "351", "dept": "CS"}
        secNocnum = {"snum": "401", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.section_manager.delete(secNocnum)[0], "Should return false when no course number is specified")
        self.assertFalse(self.section_manager.delete(secNoSnum)[0], "Should return false when no section number is specified")
        self.assertFalse(self.section_manager.delete(secNodept)[0], "Should return false when no department is specified")

    def test_edit(self):
        toEdit= {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400, "time": "1:00PM-2:00PM"}
        self.assertTrue(self.section_manager.edit(toEdit), "Edit was not successful")

    # Test edit without enough info
    def test_editNoInfo(self):
        secNocnum= {"snum": "401", "dept": "CS"}
        secNoSnum= {"cnum": "351", "dept": "CS"}
        secNodept= {"snum": "401", "cnum": "351"}
        self.assertFalse(self.section_manager.delete(secNocnum)[0], "Should return false when no course number is specified")
        self.assertFalse(self.section_manager.delete(secNoSnum)[0], "Should return false when no section number is specified")
        self.assertFalse(self.section_manager.delete(secNodept)[0], "Should return false when no department is specified")

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
        self.assertFalse(self.section_manager.edit(editDays)[0], "Should return false due to invalid days input")
        self.assertFalse(self.section_manager.edit(editIns)[0], "Should return false due to invalid instructor")
        self.assertFalse(self.section_manager.edit(editRoom)[0], "Should return false due to invalid room number")
        self.assertFalse(self.section_manager.edit(editTime)[0], "Should return false due to invalid time")

    # Need to make sure that the "time" field accepts multiple ways of inputting (e.g "01:30 PM", "1:30 PM"
    def test_editTimes(self):
        timeOne = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                    "time": "01:30PM-02:30PM", "stype": "Lecture"}
        timeTwo = {"cnum": "351", "dept": "CS", "snum": "401", "days": "MWF", "instructor": "Rock", "room": 400,
                    "time": "3:30PM-4:30PM", "stype": "Lecture"}
        self.course_manager.add({"dept": "CS", "cnum": "351"})
        self.user_manager.add({"username":"Rock", "role": dict(User.ROLES)['I']})
        self.assertTrue(self.section_manager.add(timeOne)[0], "Adding time was not successful")
        self.assertTrue(self.section_manager.edit(timeTwo)[0], "Editing time was not successful")

    # Test that if, upon editing, the if the new room and time conflict with a previously added section, it fails.
    def test_editRoomTimeConflict(self):
        newSec = {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 901, "instructor": "Gumby",
                  "days": "T", "time": "4:00PM-5:00PM"}
        self.section_manager.add(newSec)
        secConflict= {"snum" : "801", "stype": "lab", "cnum": "351", "dept": "CS", "room": 395, "instructor": "Gumby",
                  "days": "W", "time": "12:30PM-1:00PM"}
        self.assertFalse(self.section_manager.edit(secConflict)[0], "Section added conflicts with already created section")
