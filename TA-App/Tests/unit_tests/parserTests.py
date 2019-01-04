import unittest
from CmdParser import CommandParser as parser
from Managers.userManager import UserManager
from Managers.sectionManager import SectionManager
from Managers.courseManager import CourseManager
from Managers.ManagerInterface import ManagerInterface
from Managers.myStorageManager import AbstractStorageManager
from Managers.authManager import AuthManager
from TAServer.models import Course, Section, Staff as User


# This is the base class for all the testing versions of their respective classes. The main difference is in order to
# not bread the parser at runtime and maintain return types a new function has been added called getDict which returns
# the last dict passed as an argument to any of the functions. Im my eyes this is a better solution to having to return
# weird strings in the parser and having to tell the parser if its being unittested or not. Any function that normally
# returns a boolean returns False and all functions that return a string just return an empty string. (Hopefully this
# doesn't fuck everything up).
class TM(ManagerInterface):
    def __init__(self, database: AbstractStorageManager=AbstractStorageManager()):
        super().__init__(database)  # This is just so pycharm will stop being mad at me
        self.lastDict = {}  # To hold the last dict given to the class

    def add(self, fields: dict)->bool:
        self.lastDict = fields
        return False

    def view(self, fields: dict)->str:
        self.lastDict = fields
        return ""

    def edit(self, fields: dict)->bool:
        self.lastDict = fields
        return False

    def delete(self, fields: dict)->bool:
        self.lastDict = fields
        return False

    def getDict(self)->dict:
        return self.lastDict


# This is the version of CourseManager to be used for testing. The big four commands (add, view, edit, and delete) are
# all inherited from TM (because it is first in the inheritance) and reqFields and optFields come from CourseManager
# giving this testing class the best of both worlds. The code I had before (to make sure the functions I wanted) were
# being called is still there, just commented out, in the case that this doesn't work how I think it'll work. This is
# how the TCM, TSM, and TUM work.
class TCM(TM, CourseManager):
    def __init__(self, database: AbstractStorageManager=AbstractStorageManager()):
        super(TM, self).__init__(database)
        super(CourseManager, self).__init__(database)

    # def add(self, fields: dict)->bool:
    #     return TM.add(self, fields)
    #
    # def view(self, fields: dict)->str:
    #     return TM.view(self, fields)
    #
    # def edit(self, fields: dict)->bool:
    #     return TM.edit(self, fields)
    #
    # def delete(self, fields: dict)->bool:
    #     return TM.delete(self, fields)
    #
    # @staticmethod
    # def reqFields()->list:
    #     return CourseManager.reqFields()
    #
    # @staticmethod
    # def optFields()->list:
    #     return CourseManager.optFields()


# Check TCM
class TSM(TM, SectionManager):
    def __init__(self, database: AbstractStorageManager=AbstractStorageManager()):
        super(TM, self).__init__(database)
        super(SectionManager, self).__init__(database)

    # def add(self, fields: dict)->bool:
    #     return TM.add(self, fields)
    #
    # def view(self, fields: dict)->str:
    #     return TM.view(self, fields)
    #
    # def edit(self, fields: dict)->bool:
    #     return TM.edit(self, fields)
    #
    # def delete(self, fields: dict)->bool:
    #     return TM.delete(self, fields)
    #
    # @staticmethod
    # def reqFields()->list:
    #     return SectionManager.reqFields()
    #
    # @staticmethod
    # def optFields()->list:
    #     return SectionManager.optFields()


# Check TCM
class TUM(TM, UserManager):
    def __init__(self, database: AbstractStorageManager=AbstractStorageManager()):
        super(TM, self).__init__(database)
        super(UserManager, self).__init__(database)

    # def add(self, fields: dict)->bool:
    #     return TM.add(self, fields)
    #
    # def view(self, fields: dict)->str:
    #     return TM.view(self, fields)
    #
    # def edit(self, fields: dict)->bool:
    #     return TM.edit(self, fields)
    #
    # def delete(self, fields: dict)->bool:
    #     return TM.delete(self, fields)
    #
    # @staticmethod
    # def reqFields()->list:
    #     return UserManager.reqFields()
    #
    # @staticmethod
    # def optFields()->list:
    #     return UserManager.optFields()


# This test version is a little different from the rest because AuthManager does not implement the manager interface.
# This has all the same functions as AuthManager except they either return an empty string or True when appropriate.
# Except for login which returns the current user that can be set by the function setUser.
class TAM(AuthManager):
    def __init__(self, usermgr: UserManager):
        super().__init__(usermgr)
        self.user = None

    def setUser(self, u: User):
        self.user = u

    def login(self, username: str, password: str)->User:
        return self.user

    def logout(self, u: User)->str:
        return ""

    def validate(self, command: str)->bool:
        return True


# This is all the test cases. Only the big three commands are tested (course, section, and user). This only tests that
# the right helper function is called and the right params are given to the manager.
class ParserTest(unittest.TestCase):
    def setUp(self):
        self.usermgr = TUM()
        self.sectmgr = TSM()
        self.coursemgr = TCM()
        self.authmgr = TAM(self.usermgr)
        self.p = parser(self.sectmgr, self.usermgr, self.coursemgr, self.authmgr)

    def tearDown(self):
        pass

    def test_courseAdd(self):
        self.p.parse("course add code=CS-351-601")
        self.assertDictEqual(self.coursemgr.getDict(), {'dnum': 'CS', 'cnum': '351', 'snum': '601'})

    def test_courseEditByCode(self):
        pass

    def test_courseEditByNums(self):
        pass

    def test_courseViewAll(self):
        pass

    def test_courseViewOneByCode(self):
        pass

    def test_courseViewOneByNums(self):
        pass

    def test_courseDeleteByCode(self):
        pass

    def test_courseDeleteByNums(self):
        pass

    def test_sectionAdd(self):
        pass

    def test_sectionEditByCode(self):
        pass

    def test_sectionEditByNums(self):
        pass

    def test_sectionViewOneByCode(self):
        pass

    def test_sectionViewOneByNums(self):
        pass

    def test_sectionViewAll(self):
        pass

    def test_sectionDeleteByCode(self):
        pass

    def test_sectionDeleteByNums(self):
        pass

    def test_userAdd(self):
        pass

    def test_userEdit(self):
        pass

    def test_userViewOne(self):
        pass

    def test_userViewAll(self):
        pass

    def test_userDelete(self):
        pass


if __name__ == '__main__':  # Just a placeholder until a real test runner is written
    unittest.main()