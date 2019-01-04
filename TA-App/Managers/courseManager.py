from Managers.ManagerInterface import ManagerInterface
from Managers.DjangoStorageManager import DjangoStorageManager as dsm
from TAServer.models import Course

# Course obj used for CourseManger, might place in seperate file once we finalize everything

        
# Handles adding,viewing,editing and deleting of all courses.
class CourseManager(ManagerInterface):

    def __init__(self, dm: dsm, parent=None):

        # Right now only CS dept courses can be added with manager. 
        # Dept list can be changed to support more departments
        self.depts = ['CS', 'MATH']
        self.storage = dm
        if parent is None:
            from Managers.sectionManager import SectionManager as SM
            self.section_manager = SM(self.storage)
        else:
            self.section_manager = parent

    # Adds a Course to the database, returning True if added, False if not added (Error or already exists).
    def add(self, fields: dict):

        if not self._check_params(fields):
            return False, "Please fill out both dept and cnum"

        course = self.storage.get_course(dept=fields['dept'], cnum=fields['cnum'])
        if course is None:
            course = Course()
            course.dept = fields['dept']
            course.cnum = fields['cnum']
            # Unvalidated fields
            if 'name' in fields.keys() and fields['name'] is not None and len(fields['name'].strip()) > 0:
                course.name = fields['name']
            if 'description' in fields.keys() and fields['description'] is not None and len(fields['description'].strip()) > 0:
                course.description = fields['description']
            self.storage.insert_course(course)
            return True, ""
        return False, "Course already exists!"

    # Returns a list of matching courses.
    # ALWAYS returns a list, even if only one course. access by using list[0]
    # On multiple view, list of courses is sorted by dept THEN cnum eg CS240 is before MATH105
    def view(self, fields: dict)->[dict]:
        dept = None
        cnum = None
        retVal = []
        if 'dept' in fields.keys() and fields['dept'] is not None and len(fields['dept'].strip()) > 0:
            dept = fields['dept']
        if 'cnum' in fields.keys() and fields['cnum'] is not None and len(
                fields['cnum'].strip()) > 0:
            cnum = fields['cnum']
        matchingcourses = []
        if dept is not None and cnum is not None:
            matchingcourses = self.storage.get_courses_by(dept=dept, cnum=cnum)
        elif dept is not None:
            matchingcourses = self.storage.get_courses_by(dept=dept)
        elif cnum is not None:
            matchingcourses = self.storage.get_courses_by(cnum=cnum)
        else:
            matchingcourses = self.storage.get_courses_by()

        for course in matchingcourses:
            retFields = {}
            retFields['dept'] = course.dept
            retFields['cnum'] = course.cnum
            retFields['name'] = course.name
            retFields['description'] = course.description
            if 'nonrecursive' not in fields.keys():
                retFields['sections'] = self.section_manager.view({"dept":course.dept, "cnum":course.cnum, "nonrecursive": "true"})
            else:
                retFields['sections'] = ['nonrecursive']
            retVal.append(retFields)
        retVal.sort(key=lambda k: k['dept'] + k['cnum'])
        return retVal

    def delete(self, fields: dict):
        """Delete a specific course from the database"""

        # Check if required params are present and error check optional params
        if not self._check_params(fields):
            return False, "Please fill out both dept and cnum"

        # Store dict values into variables
        dept = fields.get('dept').upper()
        cnum = fields.get('cnum')

        # Retrieve courses with dept and cnum
        course_list = self.storage.get_courses_by(dept=dept, cnum=cnum)
        
        # Delete all courses retreived from database with given dept and cnum
        for c in course_list:
            if not self.storage.delete(c):
                return False, "Error Deleting Course"
        return True, ""

    # Edits a Course, returning true if successful
    def edit(self, fields: dict):

        if not self._check_params(fields):
            return False, "Please fill out both dept and cnum"

        course = self.storage.get_course(dept=fields['dept'], cnum=fields['cnum'])
        if course is not None:

            # Unvalidated fields
            if 'name' in fields.keys() and fields['name'] is not None and len(fields['name'].strip()) > 0:
                course.name = fields['name']
            if 'description' in fields.keys() and fields['description'] is not None and len(fields['description'].strip()) > 0:
                course.description = fields['description']
            self.storage.insert_course(course)
            return True, ""
        return False, "Course doesn't exist!"

    # Check for invalid parameters
    def _check_params(self, fields: dict):

        dept = fields.get('dept')
        cnum = fields.get('cnum')
        instructor = fields.get('instructor')

        if not dept:
            return False

        if not cnum:
            return False

        if not cnum.isdigit():
            return False

        else: return True

    @staticmethod
    def reqFields()->list:
        return ['dept', 'cnum']
        

    @staticmethod
    def optFields()->list:
        return ['name', 'description', 'snum', 'instructor']
