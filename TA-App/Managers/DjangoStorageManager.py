# Helper class for dealing with django's database
# See myStorageManager Interface for full documentation on method behaviors
from django.contrib.auth.models import Group
from Managers.myStorageManager import AbstractStorageManager
from TAServer.models import Course, Section, Staff as User


class DjangoStorageManager(AbstractStorageManager):

    @staticmethod
    def set_up(overwrite=False)->bool:
        retVal = False
        if len(Section.objects.all()) > 0 or len(User.objects.all()) > 0 or len(Course.objects.all()) > 0:
            # Database isn't empty!
            if not overwrite:
                retVal = False
            else:
                for section in Section.objects.all():
                    section.delete()
                for user in User.objects.all():
                    user.delete()
                for course in Course.objects.all():
                    course.delete()
                retVal = True
        sup = User(username="supervisor", password="123", role=dict(User.ROLES)["S"])
        DjangoStorageManager.insert_user(sup)
        group = Group.objects.get(name=sup.role)
        if group:
            group.user_set.add(sup)
            sup.is_superuser = True
            sup.set_password(sup.password)
        DjangoStorageManager.insert_user(sup)
        return retVal

    @staticmethod
    def insert_course(course: Course)->bool:
        existingcourse = DjangoStorageManager.get_course(dept=course.dept, cnum=course.cnum)
        overwritten = False

        # Checking if course already exists
        if existingcourse != None:
            # overwrite case, just setting new course's id to the old one we found, then overwriting
            course.id = existingcourse.id
            course.save()
            overwritten = True
        else:
            # new course, just save it
            course.save()
            overwritten = False

        return overwritten

    @staticmethod
    def insert_section(section: Section)->bool:
        existingsection = DjangoStorageManager.get_section(snum=section.snum, cnum=section.course.cnum, dept=section.course.dept)
        overwritten = False

        # Checking if section already exists
        if existingsection != None:
            # overwrite case, just setting new sections id to the old one we found, then overwriting
            section.id = existingsection.id
            section.save()
            overwritten = True
        else:
            # new section, just save it
            section.save()
            overwritten = False

        return overwritten

    @staticmethod
    def insert_user(user: User)->bool:
        existinguser = DjangoStorageManager.get_user(user.username)
        overwritten = False

        # Checking if user already exists
        if existinguser != None:
            # overwrite case, just setting new users id to the old one we found, then overwriting
            user.id = existinguser.id
            user.save()
            overwritten = True
        else:
            #new user, just save it
            user.save()
            overwritten = False

        return overwritten

    @staticmethod
    def get_users_by(username: str="", role: str = "")->[User]:
        retval = []
        query = None

        # Filtering by a value iff the value is not ""
        if username == "" and role == "":
            query = User.objects.all()
        elif username == "" and role != "":
            query = User.objects.filter(role=role)
        elif username != "" and role == "":
            query = User.objects.filter(username=username)
        elif username != "" and role != "":
            query = User.objects.filter(username=username, role=role)

        # Making the queryset a list for easier manager use
        for user in query:
            retval.append(user)

        return retval

    @staticmethod
    def get_user(username: str)->User:
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_course(dept: str, cnum: str)->Course:
        return Course.objects.filter(dept=dept, cnum=cnum).first()

    @staticmethod
    def get_courses_by(dept: str = "", cnum: str = "")->[Course]:
        retval = []
        query = None

        # Filtering by a value iff the value is not ""
        if dept != "" and cnum != "":
            query = Course.objects.filter(dept=dept, cnum=cnum)
        elif dept == "" and cnum != "":
            query = Course.objects.filter(cnum=cnum)
        elif dept != "" and cnum == "":
            query = Course.objects.filter(dept=dept)
        elif dept == "" and cnum == "":
            query = Course.objects.all()

        # Making the queryset a list for easier manager use
        for course in query:
            retval.append(course)

        return retval

    @staticmethod
    def get_section(dept: str, cnum: str, snum: str)->Section:
        return Section.objects.filter(course__cnum=cnum, course__dept=dept, snum=snum).first()

    @staticmethod
    def get_sections_by(dept: str = "", cnum: str = "", snum: str = "")->[Section]:
        retval = []
        query = None

        # Filtering by a value iff the value is not ""
        if   snum == "" and dept == "" and cnum == "":
            query = Section.objects.all()
        elif snum == "" and dept == "" and cnum != "":
            query = Section.objects.filter(course__cnum=cnum)
        elif snum == "" and dept != "" and cnum == "":
            query = Section.objects.filter(course__dept=dept)
        elif snum == "" and dept != "" and cnum != "":
            query = Section.objects.filter(course__dept=dept, course__cnum=cnum)
        elif snum != "" and dept == "" and cnum == "":
            query = Section.objects.filter(snum=snum)
        elif snum != "" and dept == "" and cnum != "":
            query = Section.objects.filter(snum=snum, course__cnum=cnum)
        elif snum != "" and dept != "" and cnum == "":
            query = Section.objects.filter(snum=snum, course__dept=dept)
        elif snum != "" and dept != "" and cnum != "":
            query = Section.objects.filter(snum=snum, course__dept=dept, course__cnum=cnum)

        # Making the queryset a list for easier manager use
        for section in query:
            retval.append(section)

        return retval

    @staticmethod
    def delete(to_delete)->bool:
        deleted = False
        if (isinstance(to_delete, Course) or isinstance(to_delete, Section) or isinstance(to_delete, User)) and to_delete.id is not None:
            to_delete.delete()
            deleted = True
        return deleted
