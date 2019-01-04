from Managers.DjangoStorageManager import DjangoStorageManager as dm
from TAServer.models import Course, Section, Staff as User
from Managers.userManager import UserManager
from Managers.courseManager import CourseManager
from Managers.sectionManager import SectionManager
from django.test import TestCase


class UserManagerTests(TestCase):

    def setUp(self):
        self.user_manager = UserManager(dm)
        self.course_manager = CourseManager(dm)
        self.section_manager = SectionManager(dm)

    def tearDown(self):
        del self.user_manager

    def test_user_add_basic(self):
        # Basic fields case
        fields = {'username':'test',
                  'password':'123'}

        # Testing that the returns are the expected behavior:
        self.assertTrue(self.user_manager.add(fields)[0], "Should be a valid user add!")
        self.assertFalse(self.user_manager.add(fields)[0], "Should no longer be able to add !: User Exists")

    def test_user_add_incorrect_fields(self):
        # Completely incorrect add, the req fields aren't filled out!
        fields = {'un': 'new',
                  'pass': 'lola'}
        self.assertFalse(self.user_manager.add(fields)[0], "Should only add if reqfields are filled out!")

        fields = {'username': 'test',
                  'password':'123',
                  'role': 'student'}
        self.assertFalse(self.user_manager.add(fields)[0], "Role provided not in ROLES! Should not add!")

    def test_user_add_complicated(self):
        # A complicated, highest level test, shouldn't fail or throw exceptions:
        fields = {'username': 'test',
                  'password': '123',
                  'role': dict(User.ROLES)["I"],  # Instructor, ins, whatever
                  'email':'foo@bar.com',
                  'address':'123 sesame street'}

        # Return val checking for subsequent calls
        self.assertTrue(self.user_manager.add(fields)[0], "Failed on omplicated user add")
        self.assertFalse(self.user_manager.add(fields)[0], "Shouldn't be able to call again")

    def test_view_user_basic(self):
        # adding basic user to test with
        fields = {'username': 'test',
                  'password': '123'}

        self.assertEqual(len(self.user_manager.view({"username":"test"})), 0, "No users case!")
        self.assertTrue(self.user_manager.add(fields)[0])
        retVal = self.user_manager.view(fields)[0]

        # Testing all values against what they should be
        self.assertEqual(retVal['username'], 'test')
        self.assertEqual(retVal['password'], '123')
        self.assertEqual(retVal['firstname'], '')
        self.assertEqual(retVal['lastname'], '')
        self.assertEqual(retVal['bio'], '')
        self.assertEqual(retVal['email'], '')
        self.assertEqual(retVal['role'], dict(User.ROLES)['D'])
        self.assertEqual(retVal['phonenum'], '')
        self.assertEqual(retVal['address'], '')

    def test_view_user_all_basic(self):
        # Adding three basic users to test with
        fields1 = {'username': 'test',
                  'password': '123'}

        fields2 = {'username': 'scotty',
                  'password': '232',
                   'role':dict(User.ROLES)["A"]}

        fields3 = {'username': 'truff',
                  'password': 'pass',
                   'role':dict(User.ROLES)["I"]}

        self.assertTrue(self.user_manager.add(fields1)[0], "Error adding fields1!")
        self.assertTrue(self.user_manager.add(fields2)[0], "Error adding fields2!")
        self.assertTrue(self.user_manager.add(fields3)[0], "Error adding fields3!")

        # View all (no username or role provided) must return all users, alphabetically sorted by username
        retVal = self.user_manager.view({})
        self.assertEqual(len(retVal), 4)

        # Because sorted by username
        retFields1 = retVal[2]
        retFields2 = retVal[0]
        retFields3 = retVal[3]

        # All retFields should not be None and must all be of type dict
        self.assertIsNotNone(retFields1)
        self.assertIsNotNone(retFields2)
        self.assertIsNotNone(retFields3)
        
        self.assertIsInstance(retFields1, dict)
        self.assertIsInstance(retFields2, dict)
        self.assertIsInstance(retFields3, dict)
        
        # Testing all values against what they should be
        self.assertEqual(retFields1['username'], 'test')
        self.assertEqual(retFields1['password'], '123')
        self.assertEqual(retFields1['firstname'], '')
        self.assertEqual(retFields1['lastname'], '')
        self.assertEqual(retFields1['bio'], '')
        self.assertEqual(retFields1['email'], '')
        self.assertEqual(retFields1['role'], dict(User.ROLES)['D'])
        self.assertEqual(retFields1['phonenum'], '')
        self.assertEqual(retFields1['address'], '')

        self.assertEqual(retFields2['username'], 'scotty')
        self.assertEqual(retFields2['password'], '232')
        self.assertEqual(retFields2['firstname'], '')
        self.assertEqual(retFields2['lastname'], '')
        self.assertEqual(retFields2['bio'], '')
        self.assertEqual(retFields2['email'], '')
        self.assertEqual(retFields2['role'], dict(User.ROLES)['A'])
        self.assertEqual(retFields2['phonenum'], '')
        self.assertEqual(retFields2['address'], '')

        self.assertEqual(retFields3['username'], 'truff')
        self.assertEqual(retFields3['password'], 'pass')
        self.assertEqual(retFields3['firstname'], '')
        self.assertEqual(retFields3['lastname'], '')
        self.assertEqual(retFields3['bio'], '')
        self.assertEqual(retFields3['email'], '')
        self.assertEqual(retFields3['role'], dict(User.ROLES)['I'])
        self.assertEqual(retFields3['phonenum'], '')
        self.assertEqual(retFields3['address'], '')
        
    def test_edit_user_basic(self):
        # Basic fields case
        fields = {'username': 'test',
                  'password': '123'}

        self.assertFalse(self.user_manager.edit(fields)[0], "No user to edit!")
        self.assertTrue(self.user_manager.add(fields)[0], "Add should work")
        # Editing nothing should still return true
        self.assertTrue(self.user_manager.edit(fields)[0], "Edit should return true if user exists! Even if no changes!")
        # Basic editing
        # Basic fields case
        fields = {'username': 'test',
                  'password': 'newpass'}
        self.assertTrue(self.user_manager.edit(fields)[0], "Edit should return true.")

    def test_edit_user_roles_and_view_integrated(self):
        # Basic fields case
        fields = {'username': 'test',
                  'password': '123'}

        self.assertTrue(self.user_manager.add(fields)[0])
        retVal = self.user_manager.view(fields)[0]
        self.assertEqual(retVal['username'], 'test')
        self.assertEqual(retVal['password'], '123')
        self.assertEqual(retVal['firstname'], '')
        self.assertEqual(retVal['lastname'], '')
        self.assertEqual(retVal['bio'], '')
        self.assertEqual(retVal['email'], '')
        self.assertEqual(retVal['role'], dict(User.ROLES)['D'])
        self.assertEqual(retVal['phonenum'], '')
        self.assertEqual(retVal['address'], '')

        # Basic fields case
        fields = {'username': 'test',
                  'password': '123',
                  'role': dict(User.ROLES)['I']}

        self.assertTrue(self.user_manager.edit(fields)[0])
        retVal = self.user_manager.view(fields)[0]
        self.assertEqual(retVal['username'], 'test')
        self.assertEqual(retVal['password'], '123')
        self.assertEqual(retVal['firstname'], '')
        self.assertEqual(retVal['lastname'], '')
        self.assertEqual(retVal['bio'], '')
        self.assertEqual(retVal['email'], '')
        self.assertEqual(retVal['role'], dict(User.ROLES)['I'])
        self.assertEqual(retVal['phonenum'], '')
        self.assertEqual(retVal['address'], '')

    def test_delete_user(self):
        # Basic fields case
        fields = {'username': 'test',
                  'password': '123'}
        self.assertTrue(self.user_manager.add(fields)[0])
        self.assertEqual(len(self.user_manager.view({"username":"test"})), 1)
        self.assertTrue(self.user_manager.delete({"username":"test"})[0])
        self.assertEqual(len(self.user_manager.view({"username":"test"})), 0, "Should have been deleted!")

    # Tests that courses and sections lists work properly
    def test_view_check_courses_and_sections(self):
        rockDict = {"username": "Rock",
                    "role":dict(User.ROLES)["I"]}
        tanawatDict = {"username": "Tanawat",
                       "role":dict(User.ROLES)["T"]}
        self.user_manager.add(rockDict)
        self.user_manager.add(tanawatDict)
        self.course_manager.add({"dept":"CS", "cnum":"361"})
        self.course_manager.add({"dept":"CS", "cnum":"557"})
        sectionFields1 = {"dept": "CS",
                          "cnum": "361",
                          "snum": "401",
                          "stype": "Lecture",
                          "instructor": "Rock"}

        sectionFields2 = {"dept": "CS",
                          "cnum": "361",
                          "snum": "801",
                          "stype": "Lab",
                          "instructor": "Tanawat"}

        sectionFields3 = {"dept": "CS",
                          "cnum": "557",
                          "snum": "401",
                          "stype": "Lecture",
                          "instructor": "Rock"}

        self.assertTrue(self.section_manager.add(sectionFields1))
        self.assertTrue(self.section_manager.add(sectionFields2))
        self.assertTrue(self.section_manager.add(sectionFields3))

        retRock = self.user_manager.view({"username":"Rock"})[0]
        retTan = self.user_manager.view({"username":"Tanawat"})[0]

        # Rock should have 2 courses and 2 sections
        self.assertEqual(len(retRock["courses"]), 2)
        self.assertEqual(len(retRock["sections"]), 2)

        # Rock's first course should be 361, and the second 557 (sorted)
        self.assertEqual(retRock["courses"][0]["cnum"], "361")
        self.assertEqual(retRock["courses"][1]["cnum"], "557")

        # Rock's first section should be 361-401 then 557-401
        self.assertEqual(retRock["sections"][0]["cnum"], "361")
        self.assertEqual(retRock["sections"][0]["snum"], "401")
        self.assertEqual(retRock["sections"][1]["cnum"], "557")
        self.assertEqual(retRock["sections"][1]["snum"], "401")
