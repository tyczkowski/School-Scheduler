import unittest
from skeleton import Project

class TestTA(unittest.TestCase):

    def setUp(self):
        self.p = Project()

        #Setup TA users
        self.p.command("user add perms=TA username=ta1 password=password")
        self.p.command("user add perms=TA username=ta2 password=password email=ta2@uwm.edu pnumber=4142321232 address=123 Maryland Ave")
    def tearDown(self):
        self.p.command("logout")

    # User Story #25 : TA: View TA assignments
    def test_ta_view_ta_assignments(self):
        self.p.command("login supervisor1 password")

        #Add course and assign TAs to sections
        self.p.command("course add dept=CS cnum=351")
        self.p.command("section add dept=CS cnum=351 snum=801")
        self.p.command("section add dept=CS cnum=351 snum=802")
        self.p.command("section edit code=CS-351-801 TA=ta1")
        self.p.command("section edit code=CS-351-802 TA=ta2")
        self.p.command("logout")

        #Login to TA account
        self.p.command("login ta1 password")

        #View assignment of second TA
        self.assertEqual("\nUsername: ta2\nRole(s): TA \nEmail: ta2@uwm.edu \nAssignments: CS-351-802" ,self.p.command("user view ta2"))

        self.p.command("logout")

        #Log in to second ta
        self.p.command("login ta2 password")

        #View Ta1 assignments
        self.assertEqual("\nUsername: ta1\nRole(s): TA \nEmail: None \nAssignments: CS-351-801" ,self.p.command("user view ta1"))


    # User Story #34 : TA: Read public contact information for all users
    def test_ta_read_public_info(self):
        self.p.command("login ta1 password")
        
        #Only display public info 
        self.assertEqual("\nUsername: ta2\nRole(s): TA \nEmail: ta2@uwm.edu",self.p.command("user view ta2"))

class TestInstructor(unittest.TestCase):

    def setUp(self):
        self.p=Project()

        #Create users
        self.p.command("user add perms=INSTRUCTOR username=instr1 password=password")
        self.p.command("user add perms=TA username=ta1 password=password")
        self.p.command("user add perms=TA username=ta2 password=password email=ta2@uwm.edu")

    def tearDown(self):
        self.p.command("logout")

    # User Story #42 : Instructor: View TA assignments
    def test_instr_view_ta_assignments(self):
        self.p.command("login supervisor1 password")

        #Add course and assign TAs to sections
        self.p.command("course add dept=CS cnum=351 instructor=instr1")
        self.p.command("section add dept=CS cnum=351 snum=801")
        self.p.command("section edit code=CS-351-802 TA=ta2")
        self.p.command("logout")

        
        self.p.command("login instr1 password")

        #ta1 should have no assignments, ta2 is assigned to CS-351 Section 802
        self.assertEqual("Username: ta1 \nRole(s): TA \nEmail: None \nAssignments: None","user view ta1")
        self.assertEqual("Username: ta2 \nRole(s): TA \nEmail:ta2uwm.edu \nAssignments: CS-351-802","user view ta2")

    # User Story #43 : Instructor: Get TA email
    def test_instr_view_ta_email(self):
        self.p.command("login instr1 password")
        self.assertEqual("Username: ta1 \nRole(s): TA \nEmail: None \nAssignments: None","user view ta1")
        self.assertEqual("Username: ta2 \nRole(s): TA \nEmail:ta2uwm.edu \nAssignments: CS-351-802","user view ta2")

    # User Story #48 : Change TA lab section
    def test_instr_change_ta_lab(self):
        self.p.command("login supervisor1 password")

        #Add course and assign TAs to sections
        self.p.command("course add dept=CS cnum=351 instructor=instr1")
        self.p.command("section add dept=CS cnum=351 snum=801")
        self.p.command("section add dept=CS cnum=351 snum=802")
        self.p.command("section edit code=CS-351-802 TA=ta2")
        self.p.command("logout")

        
        self.p.command("login instr1 password")

        #Test changes to sections
        self.assertEqual("TA section changed.",self.p.command("user edit ta2 snum=801"))
        self.assertEqual("Username: ta2 \nRole(s): TA \nEmail:None \nAssignments: CS-351-801",self.p.command("user view ta2"))
        self.assertEqual("TA section changed.",self.p.command("user edit ta2 snum=802"))
        self.assertEqual("Username: ta2 \nRole(s): TA \nEmail:None \nAssignments: CS-351-802",self.p.command("user view ta2"))