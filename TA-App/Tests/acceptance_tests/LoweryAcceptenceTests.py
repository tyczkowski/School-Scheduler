import unittest
from skeleton import Project
	
# Each of these tests assumes that the database is clear at the start of the test except for the one user 'supervisor1' with supervisor perms
class LoweryTests(unittest.TestCase):
	def setUp(self):
		p = Project() # It would be useful to have a way to specify working with a clean database in the constructor 
		p.command("login supervisor1 password")

	def tearDown(self):
		p.command("logout")

	# User Story 33: Access all user data, for the Supervisor Epic
	# Acceptance Condition: The command correctly prints our the data provided
	def test_SupAccessUser(self):
		self.assertEqual("User Added", p.command("user add perms=TA username=TDog1 password=password phonenum=1234567890")) # Adding a user
		self.assertEqual("User Added", p.command("user add perms=Admin username=Bobby password=password phonenum=2222222222 address=")) # Adding another user

		self.assertEqual("Username: TDog1\nRole: TA\nPhone Number: 1234567890", p.command("user view TDog1")) # View the data for TDog1
		self.assertEqual("Username: Bobby\nRole: Administrator\nPhone Number: 2222222222", p.command("user view bobby")) # View the data for Bobby

		self.assertEqual("Username: TDog1\nRole: TA\nPhone Number: 1234567890\n\nUsername: Bobby\nRole: Administrator\nPhone Number: 2222222222", p.command("user view")) # View all users

	# User story 52: Add a TA to lab section, for the Supervisor Epic
	# Acceptance Condition: The section command correctly prints out the data 
	def	test_SupAddTa(self):
		self.assertEqual("User Added", p.command("user add perms=TA username=TDog1 password=password phonenum=1234567890")) # Adding a user
		self.assertEqual("Course Added: CS-299", p.command("course add dept=CS cnum=299"))
		self.assertEqual("Section Added: CS-299-601", p.command("section add dept=CS cnum=299 snum=601"))

		self.assertEqual("Section for CS Course Number 299\nSection Number:601", p.command("section view code=CS-299-601"))

		self.assertEqual("TA added to section", p.command("section edit code=CS-299-601 TA=TDog1"))
		
		self.assertEqual("Section for CS Course Number 299\nSection Number:601\nTA:TDog1", p.command("section view code=CS-299-601"))


	# User story 28: Add TA to course, for the Supervisor Epic
	# Acceptance Condition: The course command correctly prints out the data 
	def	test_SupAddTa(self):
		self.assertEqual("User Added", p.command("user add perms=TA username=TDog1 password=password phonenum=1234567890")) # Adding a user
		self.assertEqual("Course Added: CS-299", p.command("course add dept=CS cnum=299"))

		self.assertEqual("CS Course 299", p.command("course view code=CS-299"))

		self.assertEqual("TA added to course", p.command("course edit code=CS-299 TA=TDog1"))
		
		self.assertEqual("CS Course 299\nTA:TDog1", p.command("section view code=CS-299"))

	# User story 49: Update TA status, for the Supervisor Epic
	# Acceptance Condition: The view command outputs the updated status of the user
	def test_SupGradeTa(self):
		self.assertEqual("User Added", p.command("user add perms=TA username=TDog1 password=password phonenum=1234567890")) # Adding a user

		self.assertEqual("Username: TDog1\nRole: TA\nPhone Number: 1234567890", p.command("user view TDog1")) # View the data for TDog1

		self.assertEqual("User updated", p.command("user edit username=TDog1 status=grader"))

		self.assertEqual("Username: TDog1\nRole: TA\nStatus: Grader\nPhone Number: 1234567890", p.command("user view TDog1")) # View the data for TDog1