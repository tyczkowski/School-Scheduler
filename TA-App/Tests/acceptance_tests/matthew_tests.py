import unittest
from skeleton import Project


class MatthewTests(unittest.TestCase):

    # before each test
    def setUp(self):
        self.p = Project()
        self.p.command("login admin1 password")

    # after each test
    def tearDown(self):
        self.p.command("logout")
        del self.p

    # User Story #23 Supervisor: Assign instructor to course
    def test_supervisor_assign_instructor_to_course(self):
        # 60 check instructor added to course

        # Given a Supervisor
        self.assertEqual(
            "User Added: FOO",
            self.p.command("user add perms=SUPERVISOR username=FOO password=abc123")
        )

        # Given an Instructor
        self.assertEqual(
            "User Added: MATTHEW",
            self.p.command("user add perms=INSTRUCTOR username=MATTHEW password=abc123")
        )

        # Given a Course
        self.assertEqual(
            "Course Added: CS-351",
            self.p.command("course add CS-351")
        )

        # When Supervisor Logged In
        self.p.command("login FOO abc123")

        # When Course Given Instructor
        self.assertEqual(
            "Course Edited: CS-351",
            self.p.command("course edit CS-351 instructor=MATTHEW")
        )

        # Then Course Should Have Instructor
        self.assertEqual(
            "Course: CS-351\n Instructor: MATTHEW",
            self.p.command("course view code=CS-351")
        )


    # User Story #40 Instructor: Edit Contact Info
    def test_instructor_edit_contact_info(self):

        # Given an Instructor
        self.assertEqual(
            "User Added: MATTHEW",
            self.p.command("user add perms=INSTRUCTOR username=MATTHEW password=abc123")
        )

        # When User Logged In
        self.p.command("login MATTHEW abc123")

        # When Change Password
        self.assertEqual(
            "User Edit: MATTHEW",
            self.p.command("user add perms=INSTRUCTOR username=MATTHEW password=123abc")
        )

        # 61 check Contact information must reflect change
        self.assertEqual(
            "\nUsername: MATTHEW\nRole(s): INSTRUCTOR \nPassword: 123abc",
            self.p.command("user view username=MATTHEW")
        )


    # User Story #41 Instructor: View Assignments
    def test_instructor_view_assignments(self):

        # Given an Instructor
        self.assertEqual(
            "User Added: MATTHEW",
            self.p.command("user add perms=INSTRUCTOR username=MATTHEW password=abc123")
        )

        # Given a Course
        self.assertEqual(
            "Course Added: CS-351",
            self.p.command("course add CS-351 instructor=MATTHEW")
        )

        # When INSTRUCTOR Logged In
        self.p.command("login MATTHEW abc123")

        # 64 check correct course assignments are returned for the user
        self.assertEqual(
            "Course: CS-351\n Instructor: MATTHEW",
            self.p.command("course view code=CS-351")
        )



    # User Story #45 Instructor: Send notifications to TA
    def test_instructor_send_notifications_to_ta(self):
        # 76 Check User receives confirmation of correctly sent email

        # Later Implementation
        self.assertEqual(2 + 2, 4)

    # User Story #51 Instructor: Read public contact information for all users
    def test_instructor_get_contact_info(self):

        # Given an Instructor
        self.assertEqual(
            "User Added: MATTHEW",
            self.p.command("user add perms=INSTRUCTOR username=MATTHEW pnumber=1234567890 password=abc123")
        )

        # When User Logged In
        self.p.command("login MATTHEW abc123")

        # Fetch User
        result = self.p.command("user view username=MATTHEW")

        # Then User should have correct public info
        self.assertEqual(
            "\nUsername: MATTHEW\nRole(s): INSTRUCTOR \nPhone: 1234567890",
            result
        )

        # 85 Check Only public information should be returned
        self.assertFalse(
            result.__contains__("Password")
        )
