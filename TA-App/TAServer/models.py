# This file is copied straight from Rock's provided code under "Skeleton code for Django" in sprint 2
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models

class Course(models.Model):
    cnum = models.CharField(max_length=4)
    dept = models.CharField(max_length=10)
    name = models.CharField(max_length=40, default="", blank=True)
    description = models.CharField(max_length=200, default="", blank=True)
    sections = models.ManyToManyField('Section', related_name='sec', blank=True)

    def __str__(self):
        course_string = "Department: "+ self.dept + " "+"Cnum: "+str(self.cnum)+ " "
        if self.name:
            print('yee')
            course_string = course_string+ "Name: "+self.name + " "
        if self.description:
            course_string = course_string+ "Description: "+self.description + " "
        return course_string

    class Meta:
        permissions = (("can_view_course", "Can view course data"),
                       ("can_edit_course", "Can edit course data"),
                       ("can_delete_course", "Can delete a course"),
                       ("can_create_course", "Can create courses"),
                       ("can_add_course", "Cam add a course"),
                       ("can_assign_ins", "Can assign instructors"))


class Section(models.Model):

    # section type
    SEC_TYPE = (
        ('lab', 'Lab'),
        ('lecture', 'Lecture'),
        (None, 'None')
    )
    # days to meet (M=Monday, T=Tuesday, W=Wednesday, H=Thursday, F=Friday)
    DAYS = (
        ('M', "Monday"),
        ('T', "Tuesday"),
        ('W', "Wednesday"),
        ('H', "Thursday"),
        ('F', "Friday"),
        ('MW', "Monday Wednesday"),
        ('TH', "Tuesday Thursday"),
        ('MWF', "Monday Wednesday Friday"),
        (None, 'None')
    )
    # section number
    snum = models.CharField(max_length=4)
    # section type (uses SEC_TYPE)
    stype = models.CharField(max_length=10, blank=True, null=True, choices=SEC_TYPE, default=None)
    # course points to course model
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    # room Number
    room = models.IntegerField(default=-1, blank=True, null=True)
    # instructor or ta
    instructor = models.ForeignKey("Staff", blank=True, null=True, on_delete=models.DO_NOTHING, default=None)
    # days of week meeting
    days = models.CharField(max_length=5, blank=True, null=True, choices=DAYS, default=None)
    # time of meeting ("05:45AM-06:00AM")
    time = models.CharField(max_length=15, blank=True, null=True, default=None)

    def __str__(self):
        sec = "" + self.course.dept + "-" + self.course.cnum + "-" + self.snum + '\n'
        if self.stype is not None:
            sec = sec + "Section type: " + self.stype + '\n'
        if self.room is not None or self.room is not -1:
            sec = sec + "room: " + str(self.room) + '\n'
        if self.instructor is not None:
            sec = sec + "Instructor: " + str(self.instructor) + '\n'
        if self.days is not None:
            sec = sec + "Time(s) :" + self.days
        if self.time is not None:
            sec = sec + " " + self.time
        return sec

    class Meta:
        permissions = (("can_create_section", "Can create sections"),
                       ("can_edit_section", "Can edit sections"),
                       ("can_delete_section", "Can delete sections"),
                       ("can_view_section", "Can view sections"),
                       ("can_assign_ta", "Can assign TA's"))


class Staff(AbstractUser):
    ROLES = (
        ('T', 'TA'),
        ('I', 'Instructor'),
        ('A', 'Administrator'),
        ('S', 'Supervisor'),
        ('D', 'Default')
    )

    # username = models.CharField(max_length=30, default="")
    # password = models.CharField(max_length=30, default="")
    firstname = models.CharField(max_length=30, default="", blank=True)
    lastname = models.CharField(max_length=30, default="", blank=True)
    bio = models.CharField(max_length=100, default="", blank=True)
    email = models.CharField(max_length=30, default="", blank=True)
    role = models.CharField(max_length=13, choices=ROLES, default="")
    sections = models.ManyToManyField(Section, blank=True) # For TA's
    courses = models.ManyToManyField(Course, blank=True) # For instructors
    phonenum = models.CharField(max_length=10, default="", blank=True)
    address = models.CharField(max_length=30, default="", blank=True)

    class Meta:
        permissions = (("can_create_user", "Can create users"),
                       ("can_edit_user", "Can edit users"),
                       ("can_edit_self", "Can edit users"),
                       ("can_delete_user", "Can delete users"),
                       ("can_view_user", "Can view users"),
                       ("can_view_private", "Can view private user data"),
                       ("can_email_all", "Can send emails to all users"),
                       ("can_email_tas", "Can send emails"))
