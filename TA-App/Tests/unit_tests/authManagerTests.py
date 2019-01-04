from typing import Optional
from Managers.myStorageManager import AbstractStorageManager as storage
from Managers.authManager import AuthManager
from TAServer.models import Course, Section, Staff as User
import unittest


class AuthManagerTests(unittest.TestCase):

    def setUp(self):
        self.user = User("foo", "abc123", "ta")
        self.storage_manager = MockStorageManager()
        self.auth_manager = AuthManager(self.storage_manager)

    def tearDown(self):
        del self.auth_manager
        del self.user

    def test_login(self):
        # given a user
        user = self.user

        # and a user_manager
        auth_manager = self.auth_manager

        # when logging in a non-existing user
        a = auth_manager.login(user.username, user.password)

        # then login result contains error
        self.assertEqual((None, "No User Available"), a)

        # when adding a non-existing user
        self.storage_manager.insert_user(user)

        # and logging in existing user with wrong password
        b = auth_manager.login(user.username, "asdf")

        # then login result contains error
        self.assertEqual((None, "Incorrect Credentials"), b)

        # when logging in existing user with correct password
        b = auth_manager.login(user.username, user.password)

        # then login result contains user
        self.assertEqual((user, "Success User Logged In"), b)

        # when logging in existing user again
        c = auth_manager.login(user.username, user.password)

        # then login result contains error
        self.assertEqual((None, "User Already Logged In"), c)

    def test_logout(self):
        # given a user
        user = self.user

        # and a user_manager
        auth_manager = self.auth_manager

        # when logging out in a non-existing user
        a = auth_manager.logout(user.username)

        # then logout result contains error
        self.assertEqual("No User Available", a)

        # when adding a non-existing user
        self.storage_manager.insert_user(user)

        # and logging out existing user
        b = auth_manager.logout(user.username)

        # then logout result contains error
        self.assertEqual("User Already Logged Out", b)

        # when logging in existing user
        c1 = auth_manager.login(user.username, user.password)

        # and logging out existing user
        c2 = auth_manager.logout(user.username)

        # then login result contains user
        self.assertEqual((user, "Success User Logged In"), c1)

        # and logout result contains msg
        self.assertEqual("Success User Logged Out", c2)


    def test_validate(self):
        # given a user
        user = self.user

        # and a user_manager
        auth_manager = self.auth_manager

        # when validating a non-existing user
        a = auth_manager.validate(user.username, "someCmd", "someAction")

        # then validate result contains false
        self.assertFalse(a)

        # when adding a non-existing user
        self.storage_manager.insert_user(user)

        # and validating non-logged-in existing user
        b = auth_manager.validate(user.username, "someCmd", "someAction")

        # then validate result contains false
        self.assertFalse(b)

        # when logging in existing-user
        c = auth_manager.login(user.username, user.password)

        # then validate result contains true
        self.assertEqual((user, "Success User Logged In"), c)

        # and validating logged-in existing user
        d = auth_manager.validate(user.username, "Course", "view")

        # then validate result contains true
        self.assertTrue(d)

        # and validating logged-in existing user
        e = auth_manager.validate(user.username, "Section", "view")

        # then validate result contains true
        self.assertTrue(e)

        # and validating logged-in existing user
        f = auth_manager.validate(user.username, "User", "view")

        # then validate result contains true
        self.assertTrue(f)

        # and validating logged-in existing user
        g = auth_manager.validate(user.username, "User", "edit")

        # then validate result contains true
        self.assertFalse(g)



class MockStorageManager(storage):

    def __init__(self):
        self.users: [User] = []
        self.courses: [Course] = []
        self.sections: [Section] = []

    def set_up(self):
        self.users.append(User("supervisor", "1234", "supervisor"))

    def insert_user(self, user: User):
        self.users.append(user)

    def delete_user(self, user: User):
        self.users.remove(user)

    def get_user(self, username) -> Optional[User]:
        return next(filter(lambda n: (n.username == username), self.users), None)

    def get_all_users(self) -> [User]:
        return self.users

    def insert_course(self, course: Course):
        self.courses.append(course)

    def delete_course(self, course: Course):
        self.courses.remove(course)

    def get_course(self, dept, cnum) -> Optional[Course]:
        return next(filter(lambda n: (n.dept == dept & n.cnum == cnum), self.courses), None)

    def get_all_courses(self) -> [Course]:
        return self.courses

    def get_all_courses_by_dept(self, dept) -> [Course]:
        return filter(lambda n: (n.dept == dept), self.courses)

    def insert_section(self, section: Section):
        self.sections.append(section)

    def delete_section(self, section: Section):
        self.sections.remove(section)

    def get_section(self, dept, cnum, snum) -> Optional[Section]:
        return next(filter(lambda n: (n.dept == dept & n.cnum == cnum & n.snum == snum), self.sections), None)

    def get_all_sections(self) -> [Section]:
        return self.sections

    def get_all_sections_by_dept(self, dept) -> [Section]:
        return filter(lambda n: (n.dept == dept), self.sections)

    def get_all_sections_by_course(self, dept, cnum) -> [Section]:
        return filter(lambda n: (n.dept == dept & n.cnum == cnum), self.sections)