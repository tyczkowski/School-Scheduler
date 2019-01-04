from Managers.courseManager import CourseManager
from TAServer.models import Section, Course, Staff as User
from Managers.DjangoStorageManager import DjangoStorageManager
from django.test import TestCase


class CourseTests(TestCase):

    def setUp(self):
        self.storage = DjangoStorageManager
        self.course_manager = CourseManager(self.storage)

    def test_add_basic(self):
        # Basic add: just return true when a new course is added, false if it exists
        fields = {"dept": "CS",
                  "cnum": "351"}
        self.assertTrue(self.course_manager.add(fields)[0])
        self.assertFalse(self.course_manager.add(fields)[0])

    def test_add_all_fields_and_view(self):
        fields = {"dept": "CS",
                  "cnum": "351",
                  "name": "Data Structures and Algorithms",
                  "description": "Lotta work"}
        self.assertTrue(self.course_manager.add(fields)[0])
        self.assertFalse(self.course_manager.add(fields)[0])

        retVal = self.course_manager.view({"dept": "CS", "cnum":"351"})[0]
        self.assertEqual(retVal["dept"], "CS")
        self.assertEqual(retVal["cnum"], "351")
        self.assertEqual(retVal["name"], "Data Structures and Algorithms")
        self.assertEqual(retVal["description"], "Lotta work")

    def test_add_edit_view(self):
        fields = {"dept": "MATH",
                  "cnum": "240",
                  "name": "Matrices and Applications"}
        self.course_manager.add(fields)
        retVal = self.course_manager.view({"dept": "MATH", "cnum": "240"})[0]
        self.assertEqual(retVal["dept"], "MATH")
        self.assertEqual(retVal["cnum"], "240")
        self.assertEqual(retVal["name"], "Matrices and Applications")

        fields["name"] = "Linear Algebra"
        self.assertFalse(self.course_manager.add(fields)[0])
        self.assertTrue(self.course_manager.edit(fields)[0])
        retVal = self.course_manager.view({"dept": "MATH", "cnum": "240"})[0]
        self.assertEqual(retVal["dept"], "MATH")
        self.assertEqual(retVal["cnum"], "240")
        self.assertEqual(retVal["name"], "Linear Algebra")

    def test_edit_view_delete_all_fields(self):
        fields = {"dept": "CS",
                  "cnum": "337"}
        self.course_manager.add(fields)
        fields["description"] = "Working with unix."
        fields["name"] = "Systems Programming"

        self.course_manager.edit(fields)
        retVal = self.course_manager.view({"dept": "CS", "cnum": "337"})[0]
        self.assertEqual(retVal["dept"], "CS")
        self.assertEqual(retVal["cnum"], "337")
        self.assertEqual(retVal["description"], "Working with unix.")
        self.assertEqual(retVal["name"], "Systems Programming")

        self.assertTrue(self.course_manager.delete({"dept":"CS", "cnum":"337"}))
        self.assertEqual(len(self.course_manager.view({"dept":"CS", "cnum": "337"})), 0)
        
    # Big test.
    def test_view_all_basic(self):
        fields1 = {"dept": "CS",
                   "cnum": "102"}
        
        fields2 = {"dept": "MATH",
                   "cnum": "240"}

        fields3 = {"dept": "CS",
                   "cnum": "337"}
        
        self.course_manager.add(fields1)
        self.course_manager.add(fields2)
        self.course_manager.add(fields3)
        
        retVal = self.course_manager.view({})
        
        self.assertEqual(len(retVal), 3)
        
        # Validating data
        retFields1 = retVal[0]
        retFields3 = retVal[1]
        retFields2 = retVal[2]

        self.assertEqual(retFields1["dept"], "CS")
        self.assertEqual(retFields1["cnum"], "102")
        self.assertEqual(retFields1["description"], "")
        self.assertEqual(retFields1["name"], "")

        self.assertEqual(retFields2["dept"], "MATH")
        self.assertEqual(retFields2["cnum"], "240")
        self.assertEqual(retFields2["description"], "")
        self.assertEqual(retFields2["name"], "")

        self.assertEqual(retFields3["dept"], "CS")
        self.assertEqual(retFields3["cnum"], "337")
        self.assertEqual(retFields3["description"], "")
        self.assertEqual(retFields3["name"], "")
