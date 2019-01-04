from django.test import TestCase
from TAServer.models import Staff, DefaultGroup, TAGroup, InsGroup, AdminGroup, SupGroup
from django.http import HttpResponse
from Managers.ManagerInterface import ManagerInterface
from Managers.myStorageManager import AbstractStorageManager
from TAServer import views


class TestManager(ManagerInterface):
    def __init__(self, database: AbstractStorageManager = None):
        ManagerInterface.__init__(self, database)
        self.lastDict = {}
        self.req = []
        self.opt = []

    def getLastDict(self)->dict:
        return self.lastDict

    def setReqFields(self, fields: list = []):
        self.req = fields

    def setOptFields(self, fields: list = []):
        self.opt = fields

    def add(self, fields: dict)->bool:
        self.lastDict = fields
        self.lastDict['function'] = 'add'
        return False

    def view(self, fields: dict)->str:
        self.lastDict = fields
        self.lastDict['function'] = 'view'
        return ""

    def edit(self, fields: dict)->bool:
        self.lastDict = fields
        self.lastDict['function'] = 'delete'
        return False

    def delete(self, fields: dict)->bool:
        self.lastDict = fields
        self.lastDict['function'] = 'delete'
        return False

    def reqFields(self)->list:
        return self.req

    def optFields(self)->list:
        return self.opt

class viewTests(TestCase):
    def createRequest(self, user: Staff, command: str = "")->HttpResponse:
        rtr = HttpResponse()
        rtr.user = user
        rtr.POST = {"command": command}

        return rtr

    def setUp(self):
        self.UserDict = {"default": Staff(), "ta": Staff(), "ins": Staff(), "admin": Staff(), "sup": Staff()}
        self.UserDict['default'].groups.add(DefaultGroup)
        self.UserDict['ta'].groups.add(TAGroup)
        self.UserDict['ins'].groups.add(InsGroup)
        self.UserDict['admin'].groups.add(AdminGroup)
        self.UserDict['sup'].groups.add(SupGroup)

    # Test fieldsToDict
    def test_ftd_code1(self):
        command = "course add code=CS-351-601"
        output = {'dnum': 'CS', 'cnum': '351', 'snum': '601', 'command': 'course', 'action': 'add'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_code2(self):
        command = "course edit code=CS-550 ins=Danny"
        output = {'dnum': 'CS', 'cnum': '550', 'command': 'course', 'action': 'edit', 'ins': 'Danny'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_desc1(self):
        command = "course edit desc=Its fun to drive"
        output = {'command': 'course', 'action': 'edit', 'desc': 'Its fun to drive'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_desc2(self):
        command = "course edit dnum=CS desc=Its fun to drive"
        output = {'dnum': 'CS', 'command': 'course', 'action': 'edit', 'desc': 'Its fun to drive'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_desc3(self):
        command = "course edit dnum=CS desc=Its fun to drive cnum=351"
        output = {'cnum': '351', 'dnum': 'CS', 'command': 'course', 'action': 'edit', 'desc': 'Its fun to drive'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_code_desc1(self):
        command = "course edit ins=Dan desc=Its fun to drive code=CS-351-601"
        output = {'cnum': '351', 'dnum': 'CS', 'snum': '601', 'command': 'course', 'action': 'edit', 'desc': 'Its fun to drive', 'ins': 'Dan'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    def test_ftd_code_desc2(self):
        command = "course edit ins=Dan code=CS-351-601 desc=Its fun to drive"
        output = {'cnum': '351', 'dnum': 'CS', 'snum': '601', 'command': 'course', 'action': 'edit', 'desc': 'Its fun to drive', 'ins': 'Dan'}
        self.assertDictEqual(views.fieldsToDict(command), output)

    # Test validate
    def test_val_default1(self):
        command = views.fieldsToDict("course view")
        self.assertTrue(views.validate(command, self.UserDict['default']))

    def test_val_default2(self):
        command = views.fieldsToDict("section view")
        self.assertTrue(views.validate(command, self.UserDict['default']))

    def test_val_default3(self):
        command = views.fieldsToDict("user add")
        self.assertFalse(views.validate(command, self.UserDict['default']))

    def test_val_default4(self):
        command = views.fieldsToDict("course add")
        self.assertFalse(views.validate(command, self.UserDict['default']))

    def test_val_ta1(self):
        command = views.fieldsToDict("user edit username=default")
        self.assertTrue(views.validate(command, self.UserDict['ta']))

    def test_val_ta2(self):
        command = views.fieldsToDict("course view")
        self.assertTrue(views.validate(command, self.UserDict['ta']))

    def test_val_ta3(self):
        command = views.fieldsToDict("user add")
        self.assertFalse(views.validate(command, self.UserDict['ta']))

    def test_val_ta4(self):
        command = views.fieldsToDict("section edit code=CS-351 ta=default")
        self.assertFalse(views.validate(command, self.UserDict['ta']))

    def test_val_ins1(self):
        command = views.fieldsToDict("section edit code=CS-351 ta=ta1")
        self.assertTrue(views.validate(command, self.UserDict['ins']))

    def test_val_ins2(self):
        command = views.fieldsToDict("section view")
        self.assertTrue(views.validate(command, self.UserDict['ins']))

    def test_val_ins3(self):
        command = views.fieldsToDict("user add")
        self.assertFalse(views.validate(command, self.UserDict['ins']))

    def test_val_ins4(self):
        command = views.fieldsToDict("section add")
        self.assertFalse(views.validate(command, self.UserDict['ins']))

    def test_val_admin1(self):
        command = views.fieldsToDict("course add")
        self.assertTrue(views.validate(command, self.UserDict['admin']))

    def test_val_admin2(self):
        command = views.fieldsToDict("user edit")
        self.assertTrue(views.validate(command, self.UserDict['admin']))

    def test_val_admin3(self):
        command = views.fieldsToDict("section edit ta=ta1")
        self.assertFalse(views.validate(command, self.UserDict['admin']))

    def test_val_admin4(self):
        command = views.fieldsToDict("course edit ins=ins1")
        self.assertFalse(views.validate(command, self.UserDict['admin']))

    def test_val_sup1(self):
        command = views.fieldsToDict("course create")
        self.assertTrue(views.validate(command, self.UserDict['sup']))

    def test_val_sup2(self):
        command = views.fieldsToDict("user edit")
        self.assertTrue(views.validate(command, self.UserDict['sup']))

    def test_val_sup3(self):
        command = views.fieldsToDict("section edit code=CS-351 ta=ta1")
        self.assertTrue(views.validate(command, self.UserDict['sup']))

    def test_val_sup4(self):
        command = views.fieldsToDict("course edit code=CS-351 ins=ins1")
        self.assertTrue(views.validate(command, self.UserDict['sup']))

    # Test mgr
    def test_mgr1(self):
        pass