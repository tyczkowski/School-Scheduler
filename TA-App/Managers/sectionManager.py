from Managers.DjangoStorageManager import DjangoStorageManager as dsm
from Managers.userManager import UserManager as UM
from Managers.ManagerInterface import ManagerInterface
from TAServer.models import Course, Section, Staff as User


class SectionManager(ManagerInterface):

    def __init__(self, db : dsm, parent=None):
        self.db = db
        self.user_manager = UM(self.db)
        if parent is None:
            from Managers.courseManager import CourseManager as CM
            self.course_manager = CM(self.db, self)
        else:
            self.course_manager = parent

    def add(self, fields: dict):

        # check if user inputs information needed for adding
        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "addition")
        if invalid != "okay":
            return False, invalid

        # Make sure course already exists
        if not self.courseExists(cnum=fields.get("cnum"), dept=fields.get("dept")):
            return False, "Corresponding course does not exist!"

        course = self.db.get_course(dept=fields.get("dept"), cnum=fields.get("cnum"))

        # Make sure section doesn't already exist (Should be edit instead)
        if self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            return False, "Section already exists!"

        if not self.checkSnum(fields.get('snum')):
            return False, self.checkSnum(fields.get('snum'))

        snum = fields.get('snum')

        # Make sure user exists if inst is to be added
        if fields.get('instructor') is not None and len(fields.get('instructor').strip()) > 0 and not self.userExists(fields.get('instructor')):
            return False, "User doesn't exist!"

        # Check days
        if fields.get("days") is not None and len(fields.get('days').strip()) > 0 and not self.checkDays(fields.get("days")):
            return False, "Days format not accepted!"

        # Check for correct time format of start and end time
        if fields.get("time") is not None and len(fields.get('time').strip()) > 0 and not self.timeFormat(fields.get('time')) :
            return False, "Time format not accepted!"

        time = fields.get('time')
        if fields.get("days") is not None and len(fields.get('days').strip()) > 0:
            days = fields.get('days').upper()
        else:
            days = ""

        room = -1
        # try to convert room into integers
        if fields.get("room") is not None and len(fields.get("room").strip()) > 0:
            try:
                room = int(fields.get("room").strip())
            except ValueError:
                return False, "Room is not a valid integer!"

            # Check if time and room conflict
            if not self.roomConflict(time=time, room=room, days=days, sec=self.db.get_section(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")), action="add"):
                return False, "Room taken for that day/time!"

        # With and without instructor adding to course and sections db
        if fields.get('instructor') is None or len(fields.get('instructor').strip()) == 0:
            toAdd = Section(course=course, snum=snum, stype=fields.get("stype"), days=fields.get("days"),
                            room=room, time=time)
            self.addHelper(toAdd)
            return True, ""
        else:
            if not self.valUser(fields.get("instructor"), fields.get("stype")):
                return False, "Error"
            ins = self.db.get_user(username=fields.get("instructor"))
            toAdd = Section(course=course, snum=snum, stype=fields.get("stype"), days=fields.get("days"),
                            room=room, time=time, instructor=ins)
            self.addHelper(toAdd)
            return True, ""

    # Returns a list of matching sections.
    # ALWAYS returns a list, even if only one section. access by using list[0]
    # On multiple view, list of courses is sorted by dept THEN cnum THEN snum eg CS-240-401 is before MATH-105-401
    def view(self, fields: dict)->[dict]:
        dept = None
        cnum = None
        snum = None
        retVal = []
        
        if 'dept' in fields.keys() and fields['dept'] is not None and len(fields['dept'].strip()) > 0:
            dept = fields['dept']
        if 'cnum' in fields.keys() and fields['cnum'] is not None and len(
                fields['cnum'].strip()) > 0:
            cnum = fields['cnum']
        if 'snum' in fields.keys() and fields['snum'] is not None and len(
                fields['snum'].strip()) > 0:
            snum = fields['snum']
            
        matchingsections = []
        if dept is not None and cnum is not None and snum is not None:
            matchingsections = self.db.get_sections_by(dept=dept, cnum=cnum, snum=snum)
        elif dept is not None and cnum is not None and snum is None:
            matchingsections = self.db.get_sections_by(dept=dept, cnum=cnum)
        elif dept is not None and cnum is None and snum is not None:
            matchingsections = self.db.get_sections_by(dept=dept, snum=snum)
        elif dept is not None and cnum is None and snum is None:
            matchingsections = self.db.get_sections_by(dept=dept)
        elif dept is None and cnum is not None and snum is not None:
            matchingsections = self.db.get_sections_by(cnum=cnum, snum=snum)
        elif dept is None and cnum is not None and snum is None:
            matchingsections = self.db.get_sections_by(cnum=cnum)
        elif dept is None and cnum is None and snum is not None:
            matchingsections = self.db.get_sections_by(snum=snum)
        elif dept is None and cnum is None and snum is None:
            matchingsections = self.db.get_sections_by()

        for section in matchingsections:
            retFields = {}
            course = section.course
            retFields['dept'] = course.dept
            retFields['cnum'] = course.cnum
            retFields['snum'] = section.snum
            retFields['stype'] = section.stype
            if section.instructor is not None:
                retFields['instructor'] = section.instructor.username
            else:
                retFields['instructor'] = "None"
            retFields['days'] = section.days
            retFields['time'] = section.time
            retFields['room'] = section.room.__str__()
            # This is a course dict representation
            if 'nonrecursive' not in fields.keys():
                retFields['course'] = self.course_manager.view({"dept":course.dept, "cnum":course.cnum, 'nonrecursive': "true"})[0]
            else:
                retFields['course'] = {"nonrecursive":"true"}
            retVal.append(retFields)

        retVal.sort(key=lambda k: k['dept'] + k['cnum'] + k['snum'])
        return retVal


    # Edit will need cnum, snum and dept (like all other commands)
    # Any other fields specified that aren't above(e.g. room, instructor, ect.) will replace what is already in the section
    # You can not change cnum and dept, but if you want to change snum use key "snumNew" as a replacement
    def edit(self, fields: dict):

        # check if user inputs information needed for adding
        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "addition")
        if invalid != "okay":
            return False, invalid

        # Make sure course already exists
        if not self.courseExists(cnum=fields.get("cnum"), dept=fields.get("dept")):
            return False, "Course does not exist!"

        course = self.db.get_course(fields.get("dept"), fields.get("cnum"))

        # Make sure section exists
        if not self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            return False, "Section does not exist!"

        if not self.checkSnum(fields.get('snum')):
            return False, self.checkSnum(fields.get('snum'))

        snum = fields.get('snum')

        if fields.get('instructor') is not None and len(fields.get('instructor').strip()) > 0 and fields.get('instructor') != 'None' and not self.userExists(fields.get('instructor')):
            return False, "User doesn't exist!"

        # Check days
        if fields.get("days") is not None and len(fields.get('days').strip()) > 0 and not self.checkDays(fields.get("days")):
            return False, "Days format not accepted!"

        # Check for correct time format of start and end time
        if fields.get("time") is not None and len(fields.get('time').strip()) > 0 and not self.timeFormat(fields.get('time')) :
            return False, "Time format not accepted!"

        time = fields.get('time')
        if fields.get("days") is not None and len(fields.get('days').strip()) > 0:
            days = fields.get('days').upper()
        else:
            days = ""

        room = -1
        # try to convert room into integers
        if fields.get("room") is not None and len(fields.get("room").strip()) > 0:
            try:
                room = int(fields.get("room").strip())
            except ValueError:
                return False, "Room not a valid integer!"

            # Check if time and room conflict
            if not self.roomConflict(time=time, room=room, days=days, sec=self.db.get_section(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")), action="edit"):
                return False, "Room conflict!"

        # With and without instructor adding to course and sections db
        if fields.get('instructor') is None or fields.get('instructor') == 'None' or len(fields.get('instructor').strip()) == 0:
            toAdd = Section(course=course, snum=snum, stype=fields.get("stype"), days=fields.get("days"),
                            room=room, time=time)
            self.editHelper(sec=toAdd, snumNew=fields.get("snumNew"))
            return True, ""
        else:
            if not self.valUser(fields.get("instructor"), fields.get("stype")):
                return False, "Error"
            ins = self.db.get_user(fields.get("instructor"))
            toAdd = Section(course=course, snum=snum, stype=fields.get("stype"), days=fields.get("days"),
                            room=room, time=time, instructor=ins)
            self.editHelper(sec=toAdd, snumNew=fields.get("snumNew"))
            return True, ""

    def delete(self, fields: dict)->bool:

        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "deletion")
        if invalid != "okay":
            return False, invalid

        if self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            section = self.db.get_section(cnum=fields.get("cnum"),dept=fields.get("dept"), snum=fields.get("snum"))
            test = self.db.delete(section)
            if test:
                return True, ""
            else:
                return False, "Error deleting section!"
        else:
            return False, "Section does not exist!"



    # Make sure user exists
    def userExists(self, ins):
        user = self.db.get_user(username=ins)
        return user is not None

    # Make sure course exists
    def courseExists(self, cnum, dept):
        course = self.db.get_course(cnum=cnum, dept=dept)
        return course is not None

    # Make sure section exists
    def sectionExists(self,cnum, dept, snum):
        section = self.db.get_section(cnum=cnum, dept=dept, snum=snum)
        return section is not None

    # make sure necessary fields are not set to None
    def actionHelper(self, dept, cnum, snum, action):
        okay = ""
        switch = {
            dept: "Could not complete " + action + ", department is needed",
            cnum: "Could not complete " + action + ", course number is needed",
            snum: "Could not complete " + action + ", section number is needed"
        }
        return switch.get(None, "okay")

    # I expanded this helper method to also handle user lists of courses, sections. Also course lists of sections
    def addHelper(self, sec: Section):
        self.db.insert_section(sec)
        sec.course.sections.add(sec)

        # Keeping instructor fields updated
        if sec.instructor is not None:
            sec.instructor.sections.add(sec)
            if sec.course not in sec.instructor.courses.all():
                sec.instructor.courses.add(sec.course)
            self.db.insert_user(sec.instructor)

        self.db.insert_course(sec.course)
        self.db.insert_section(sec)

    def editHelper(self, sec: Section, snumNew: str):
        # Check fields that are empty from sec and set them to whatever the current section has
        # Users need to explicitly enter "None" to edit the value to None/default
        toChange = self.db.get_section(cnum=sec.course.cnum, dept=sec.course.dept, snum=sec.snum)

        # if sec.stype is None:
        #     sec.stype = toChange.stype
        # if sec.days is None:
        #     sec.days = toChange.days
        # if sec.time is None:
        #     sec.time = toChange.time
        # if sec.room is None:
        #     sec.room = toChange.room
        # if sec.instructor is None:
        #     sec.instructor = "None"

        # remove old section and replace with the new one
        self.db.insert_section(sec)
        sec.course.sections.add(sec)

        # Keeping instructor fields updated
        if sec.instructor is not None:
            sec.instructor.sections.add(sec)
            if sec.course not in sec.instructor.courses.all():
                sec.instructor.courses.add(sec.course)
            self.db.insert_user(sec.instructor)

        self.db.insert_course(sec.course)
        self.db.insert_section(sec)

    # Make sure user is a TA or instructor
    def valUser(self, ins, sectype):
        user = self.db.get_user(ins)
        if user.role != dict(User.ROLES)['T'] and user.role != dict(User.ROLES)['I']:
            # Neither TA or instructor(Professor), can't teach anything
            return False
        elif user.role == dict(User.ROLES)['T'] and sectype != dict(Section.SEC_TYPE)['lab']:
            # TAs may only teach labs
            return False
        elif user.role == dict(User.ROLES)['I'] and sectype != dict(Section.SEC_TYPE)['lecture']:
            # Professors may only teach lectures
            return False
        else:
            return True

    # Check if days are correct
    def checkDays(self, days=None):
        if days is None:
            return True
        switch = {
            'M': "fine",
            'T': "fine",
            'W': "fine",
            'H': "fine",
            'F': "fine",
            'MW': "fine",
            'TH': "fine",
            'MWF': "fine",
        }
        if switch.get(days.upper(), "Wrong") == "Wrong":
            return False
        else:
            return True

    # check the time input to make sure it's in the correct format 12:20 PM
    def timeFormat(self, time : str)->bool:
        #Note: strip string before passing
        if time is  None:
            return True
        broken = time.split("-")
        if len(broken) is not 2:
            return False

        if len(broken[0]) > 7 or len(broken[0]) < 6:
            return False
        if len(broken[1]) > 7 or len(broken[1]) < 6:
            return False

        startMinHr = broken[0].split(":")   # split 12:00PM
        if len(startMinHr) is not 2:
            return False
        startHr = startMinHr[0]             # 12
        minMer = startMinHr[1]              # 00PM
        startMin = minMer[0:2]              # 00
        startMer = minMer[2:4]              # PM

        endMinHr = broken[1].split(":")
        if len(endMinHr) is not 2:
            return False
        endHr = endMinHr[0]
        minMer = endMinHr[1]
        endMin = minMer[0:2]
        endMer = minMer[2:4]


        #check if min has  2 characters (1:5 pm or 1:0 pm will not be accepted) and hr has at least one but not more than 2 (01:30 or 1:30 is fine)
        if len(startMin) != 2 or len(startHr) > 2 or len(startHr) < 1:
            return False
        if len(endMin) != 2 or len(endHr) > 2 or len(endHr) < 1:
            return False

        # try to convert two strings into integers (minute and hour)
        try:
            startMin = int(startMin)
            startHr = int(startHr)
            endMin = int(endMin)
            endHr = int(endHr)
        except ValueError:
            print ('Time is not a valid integer')
            return False

       # for min and Hr, check appropriate range
        if startMin < 0 or startMin >= 60:
            return False
        if startHr < 1 or startHr > 12:
            return False
        if endMin < 0 or endMin >= 60:
            return False
        if endHr < 1 or endHr > 12:
            return False

        # check if the second half of the original split string broken[1] should be
        # either am or pm (lower case)

        if startMer.lower() == "am" or startMer.lower() == "pm":
            if endMer.lower() == "am" or endMer.lower() == "pm":
                return True
            else:
                return False
        else:
            return False

    # This helper will take a time in string format and return a integer time
    # The integer will be in military hours for easy comparison in roomConflict()
    # NOTE: time format should be called before calling this method or else int() conversion will fail
    def intTime(self, time: str)->list:

        broken = time.split("-")

        startMinHr = broken[0].split(":")
        startHr = startMinHr[0]             # 12
        minMer = startMinHr[1]              # 00PM
        startMin = minMer[0:2]              # 00
        startMer = minMer[2:4]              # PM

        endMinHr = broken[1].split(":")
        endHr = endMinHr[0]
        minMer = endMinHr[1]
        endMin = minMer[0:2]
        endMer = minMer[2:4]

        startMin = int(startMin)
        startHr = int(startHr)
        endMin = int(endMin)
        endHr = int(endHr)

        # convert to military time
        if startMer.lower() == "pm" and startHr != 12:
            startHr = startHr + 12
        elif startMer.lower() == "am" and startHr == 12:
            startHr = 0
        if startMin == 0:
            startMin = "00"
        else:
            startMin = str(startMin)

        startHr = str(startHr)
        startTime = startHr + startMin
        startTime = int(startTime)

        if endMer.lower() == "pm" and endHr != 12:
            endHr = endHr + 12
        elif endMer.lower() == "am" and endHr == 12:
            endHr = 0
        if endMin == 0:
            endMin = "00"
        else:
            endMin = str(endMin)

        endHr = str(endHr)
        endTime = endHr + endMin
        endTime = int(endTime)
        return [startTime, endTime]

    # NOTE: timeFormat() should be called before calling this method
    def roomConflict(self, time: str, room: int, days: str, sec: Section, action: str)->bool:

        if time is None or len(time) == 0 or room <= 0 or days is None or len(days) == 0:
            return True

        roomUse = Section.objects.filter(room=room)
        if roomUse.count() > 0:

            # get integer values for start and end times for comparison
            checkTime = self.intTime(time)
            startTime = checkTime[0]
            endTime = checkTime[1]
            posConflict = self.conDays(days)

            for x in roomUse:
                # Need to make certain not to compare the same object on edit, this shouldn't happen with add
                if sec != x and action=="edit":
                    if x.days in posConflict and x.time is not None or x.time is not "":
                        xTime = self.intTime(x.time)
                        xStart = xTime[0]
                        xEnd = xTime[1]

                        # check if start and end time is between each other class that shares the same room
                        if xStart <= startTime <= xEnd:
                            return False
                        elif xStart <= endTime <= xEnd:
                            return False
                elif action=="add":
                    if x.days in posConflict and x.time is not None or x.time is not "":
                        xTime = self.intTime(x.time)
                        xStart = xTime[0]
                        xEnd = xTime[1]

                        # check if start and end time is between each other class that shares the same room
                        if xStart <= startTime <= xEnd:
                            return False
                        elif xStart <= endTime <= xEnd:
                            return False

        return True

    # used to check time conflict, returns a list of possible days that would have a room conflict
    def conDays(self, days: str):

        switch = {
            'M': ['M','MW','MWF'],
            'T': ['T', 'TH'],
            'W': ['W', 'MW', 'MWF'],
            'H': ['H', 'TH'],
            'F': ['F', 'MWF'],
            'MW': ['M','W','MW','MWF'],
            'MWF':['M','W','F','MW','MWF'],
            'TH':['T','H','TH'],
        }

        return switch.get(days)

    def checkSnum(self, snum):
        try:
            snum = int(snum)
        except ValueError:
            return False, "Snum must be integer format!"

        # section number should be greater than 0
        if snum < 1:
            return False, "Snum must be positive!"
        else:
            return True, ""

    @staticmethod
    def reqFields()->list:
        return ["dept", "cnum", "snum"]

    # Note: "snumNew" will only do something if the user calls edit and wants to change the section number
    @staticmethod
    def optFields()->list:
        return ["instructor", "stype", "days", "room", "time"]
