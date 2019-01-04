import unittest
from skeleton import Project

#Tested against new database
class CarpioTests(unittest.TestCase):

    #User Story #16: Admins may create classes
    def test_admin_create_classes(self):
        p = Project()
        p.command("login admin1 password")
        #Using code and fields should both work!
        #Adding courses
        self.assertEqual("Course Added: CS-351", p.command("course add CS-351"))
        self.assertEqual("Course Added: CS-317", p.command("course add dept=CS cnum=317"))

        #Adding Sections
        self.assertEqual("Section Added: CS-351-401", p.command("section add CS-351-401"))
        self.assertEqual("Section Added: CS-351-801", p.command("section add dept=CS cnum=351 snum=801"))

        #Section can't exists if root course doesn't (No corresponding cnum)
        self.assertEqual("Can't Create Section, Course Doesn't Exist: CS-315", p.command("section add CS-315-801"))

        #Proper display of courses
        self.assertEqual("Course: CS-351\nSection(s): 401, 801\n", p.command("course view code=CS-351"))
        self.assertEqual("Course: CS-317\nSections(s): \n", p.command("course view CS-317"))


    #User Story #29: Admin may delete accounts
    def test_admin_delete_accounts(self):
        p = Project()
        p.command("login admin1 password")
        #Adding
        self.assertEqual("User Added: JB", p.command("user add perms=TA username=JB password=123456789"))
        #Removing
        self.assertEqual("User Removed: JB", p.command("user remove username=JB"))
        #User should no longer exist
        self.assertEqual("User Does Not Exist: JB", p.command("user view username=JB"))

        p.command("logout")

    #User Story #39 Admins may create accounts
    def test_admin_create_accounts(self):
        p = Project()
        p.command("login admin1 password")
        #Adding users
        self.assertEqual("User Added: JB", p.command("user add perms=TA username=JB password=123456789"))
        #Proper Display, user has in fact been created
        self.assertEqual("Username: JB\nRole(s): TA")

        p.command("logout")

    #User Story #46: Admins may edit account data
    def test_admin_edit_accounts(self):
        p = Project()
        p.command("login admin1 password")
        #Adding user
        self.assertEqual("User Added: JB", p.command("user add perms=TA username=JB password=123456789"))
        #Editing user (including both existsing and missing attributes)
        self.assertEqual("User Modified: JB", p.command("user edit username=JB perms=Admin pnumber=4145557777"))
        #Proper display after updating
        self.assertEqual("Username: JB\nRoles(s): Admin\nPhone Number: 4145557777")

        p.command("logout")

    #User Story #47: Admins may send email notifications
    def test_admin_email(self):
        p = Project()
        p.command("login admin1 password")
        #To be implemented

        p.command("logout")

    #User Story #50: Admins may access all system data
    def test_admin_access(self):
        p = Project()
        p.command("login admin1 password")
        #Adding user with many public and private attributes
        self.command("User Added: JB", p.command("user add perms=TA username=JB password=123456789 pnumber=4147775555 address = 123 Kirkwood"))
        #Admins should be able to view all data a user has (private and public), save the password
        self.command("Username: JB\n Roles(s): TA\nPhone Number: 4147775555\nAddress: 123 Kirkwood")

        p.command("logout")
