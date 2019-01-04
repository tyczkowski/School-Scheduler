import unittest
from Skeleton import Project


# Test TA method
class TestTA(unittest.TestCase):

    # Edit contact info #15
    def Login(self):
        mySetup = Project()

        mySetup.command("login King password1")
        mySetup.command("user add perms=TA username=Lars password=password2")
        mySetup.command("logout")

        self.assertEqual(mySetup.command("login Lars password2"), "Login successful",
                         "Test failed. Should not have been able to edit without logging in")

    def editContactInfo(self):

        mySetup = Project()

        # create TA first
        mySetup.command("login King password1")
        mySetup.command("user add perms=TA username=Lars password=password2")
        mySetup.command("logout")

        # TA edits phone number
        mySetup.command("login Lars password2")
        self.assertEqual(mySetup.command("user edit phone=(414)883-4893"),
                         "Lars successfully changed phone number to (414)883-4893",
                         "Test failed. Unable to edit phone number")
        mySetup.command("logout")


class TestSupervisor(unittest.TestCase):

    # Test logging in
    def Login(self):

        mySetup = Project()

        self.assertEqual(mySetup.command("login King password1"),
                         "Login successful",
                         "Test failed. Could not log in")

    # Test a successful add for each role
    def createUserSuccess(self):
        mySetup = Project()
        mySetup.command("login King")
        self.assertEqual(mySetup.command("user add perms=student username=Momo password=Cram"),
                         "Momo successfully added", "user was not successfully added")
        mySetup.command("logout")

    # Add course #22
    def courseSuccessAdd(self):
        mySetup = Project()
        mySetup.command("login King password1")
        self.assertEqual(mySetup.command("course add dept=CS cnum=251"),
                         "Course Added: CS-251", "Test Failed. Course was not successfully added")
        mySetup.command("logout")

    # account edit by supervisor #30
    def accountEdit(self):
        mySetup = Project()

        # edit role
        mySetup.command("login King password1")
        self.assertEqual(mySetup.command("user edit Momo role=TA"),
                         "Successfully changed Momo role to TA", "Test Failed. Role was not successfully changed")


    # Test different account changes
    def accountChanges(self):
        mySetup = Project()

        mySetup.command("login King password1")
        self.assertEqual(mySetup.command("user edit Lars officehrs=9:00AM-10:30AM"),
                         "Lars office hours successfully changed",
                         "Test Failed. Nono should have been changed to TA")
        mySetup.command("logout")

    # Test delete with supervisor #31
    def deleteAccount(self):
        mySetup = Project()

        mySetup.command("login King password1")
        self.assertEqual(mySetup.command("user delete Lars"), "Lars successfully removed",
                         "User could not be removed successfully")
        mySetup.command("logout")


# Test that any user's ability to view a specific course #99
class TestAll(unittest.TestCase):


    # create course and test view with supervisor
    def successView(self):
        mySetup = Project()

        mySetup.command("login King password1")
        mySetup.command("course add CS-417")
        self.assertEqual(mySetup.command("course view CS-417"),
                         "Course: CS-417\nSections: None\nInstructor: None\nTA: None, ",
                         "Test failed. Course could not be viewed by Supervisor")

        # add users for next tests
        mySetup.command("user add perms=TA username=Lars password=password2")
        mySetup.command("user add perms=administrator username=Sec password=password3")
        mySetup.command("user add perms=student username=Momo password=Cram")
        mySetup.command("user logout King")

        # Test view with TA
        mySetup.command("login Lars password2")
        self.assertEqual(mySetup.command("course view CS-417"),
                         "Course: CS-417\nSections: None\nInstructor: None\nTA: None, ",
                         "Test failed. Course could not be viewed by TA")
        mySetup.command("user logout Lars")

        # Test view with Student
        mySetup.command("login Momo Cram")
        self.assertEqual(mySetup.command("course view CS-417"),
                         "Course: CS-417\nSections: None\nInstructor: None\nTA: None, ",
                         "Test failed. Course could not be viewed by Student")
        mySetup.command("logout")

        # Test view with Administrator
        mySetup.command("login Sec password3")
        self.assertEqual(mySetup.command("course view CS-417"),
                         "Course: CS-417\nSections: None\nInstructor: None\nTA: None, ",
                         "Test failed. Course could not be viewed by Administrator")
        mySetup.command("logout")


