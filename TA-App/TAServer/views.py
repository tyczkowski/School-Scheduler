# This file is copied straight from Rock's provided code under "Skeleton code for Django" in sprint 2

from django.views import generic
from django.shortcuts import render, redirect
from django.views import View
from Managers.userManager import UserManager as UM
from Managers.sectionManager import SectionManager as SM
from Managers.courseManager import CourseManager as CM
from Managers.ManagerInterface import ManagerInterface
from TAServer.models import Course
from Managers.DjangoStorageManager import DjangoStorageManager as Storage # Change to whatever we're using now
from TAServer.models import Staff as User
from django.contrib.auth import authenticate, login, logout
from TAServer.forms import SignUpForm


class UserView(View):
    def view(self, request, code=""):
        print(request.GET)

        fields = {}
        template = "user/viewpublic.html" # The default is just to load only public data

        if request.user.is_authenticated and request.user.has_perm('TAServer.can_view_private'):
            template = "user/viewprivate.html"

        if code != "":
            fields['title'] = "View %s" % code
            fields['data'] = UM(Storage()).view({'username': code})

        else:
            fields['title'] = "View All Users"
            fields['data'] = UM(Storage()).view({})

        fields['datafound'] = len(fields['data']) != 0

        fields['display_edit_link'] = request.user.has_perm("TAServer.can_edit_user")

        return render(request, template, fields)

    def add(self, request, code=""):
        rolelist = ['TA', 'Instructor', 'Administrator', 'Supervisor']
        fields = {'title': 'Add a new user', 'canedit': False, "role_list": rolelist, 'checked_role': rolelist[0], 'action': '/user/add/'}

        if request.user.has_perm("TAServer.can_create_user"):
            fields['canedit'] = True

        else:
            fields['value'] = {'username': 'Bad Permissions'}

        return render(request, "user/add.html", fields)

    def edit(self, request, code="", fields={}):
        if code == "":
            return self.add(request)

        rolelist = ['TA', 'Instructor', 'Administrator', 'Supervisor']
        fields['role_list'] = rolelist

        fields['action'] = '/user/edit/%s/' % code

        fields['canedit'] = request.user.has_perm("TAServer.can_edit_user") or (request.user.username == code and request.user.has_perm("TAServer.can_edit_self"))

        if fields['canedit']:
            fields['value'] = UM(Storage()).view({'username': code})[0]
            fields['checked_role'] = fields['value']['role']

        else:
            fields['value'] = {'username': 'Bad Permissions'}

        return render(request, "user/add.html", fields)

    def get(self, request, code=""):
        print(request.GET)

        action = request.path.split("/")[2].lower()  # The 'action' of the url (view, add, edit)

        # Just a loop through the different helper functions until the action lines up with a helper function we have.
        for fun in [self.view, self.add, self.edit]:
            if fun.__name__ == action:
                return fun(request, code=code)

        return render(request, "main/index.html") # Should be changed to go to a 404 (django might do this automatically

    def post(self, request, code=""):
        print(request.POST)
        for key in request.POST:
            print("Key: %s\nValue: %s\nTypeof: %s\n" % (key, request.POST[key], type(request.POST[key])))

        rtr = ""

        if "edit" in request.path:
            rtr = UM(Storage()).edit(request.POST)

        elif "add" in request.path:
            rtr = UM(Storage()).add(request.POST)

        else:
            print("Someone sent a post fron %s" % request.path)

        print(rtr)

        status = ""

        if rtr[0]:
            status = "Added Correctly"
        else:
            status = rtr[1]

        return self.edit(request, code=request.POST['username'], fields={'displaystatus': True, 'status': status})  # Just a placeholder


class CourseViews(View):

    def add(self, request, code=""):
        return render(request, "courses/course_add.html")

    def edit(self, request, code=""):
        course = CM(Storage()).view({'dept': code[:2], 'cnum': code[2:]})
        return render(request, "courses/course_edit.html", {'course': course[0]})

    def view(self, request, code=""):
        print(SM(Storage()).view({}))
        courses = CM(Storage()).view({})
        return render(request, "courses/course_list.html", {'courses': courses})

    def detail(self, request, code=""):
        course = CM(Storage()).view({'dept': code[:2], 'cnum': code[2:]})
        return render(request, "courses/course_detail.html", {'course': course[0]})


    def get(self, request, code=""):
        action = request.path.split("/")[2].lower()
        for fun in [self.add, self.edit, self.view, self.detail]:
            if fun.__name__ == action:
                return fun(request, code=code)

        return render(request, "404.html")

    def post(self, request, code=""):
        print(request.POST)

        if "edit" in request.path:
            CM(Storage()).edit(request.POST)

        elif "add" in request.path:
            CM(Storage()).add(request.POST)

        return redirect('/courses/view')

class SectionViews(View):

    def add(self, request, code=""):
        return render(request, "sections/section_add.html")

    def edit(self, request, code=""):
        section = SM(Storage()).view({'cnum': code[:3], 'snum': code[3:]})
        return render(request, "sections/section_edit.html", {'section': section[0]})

    def view(self, request, code=""):
        sections = SM(Storage()).view({})
        return render(request, "sections/section_list.html", {'sections': sections})

    def detail(self, request, code=""):
        section = SM(Storage()).view({'cnum': code[:3], 'snum': code[3:]})
        return render(request, "sections/section_detail.html", {'section': section[0]})

    def get(self, request, code=""):
        action = request.path.split("/")[2].lower()
        for fun in [self.add, self.edit, self.view, self.detail]:
            if fun.__name__ == action:
                return fun(request, code=code)

        return render(request, "404.html")

    def post(self, request, code=""):
        print(request.POST)
        res = ""
        if "edit" in request.path:
            res = SM(Storage()).edit(request.POST)

        elif "add" in request.path:
            res = SM(Storage()).add(request.POST)
        print(res)
        return redirect('/sections/view')

class AssignSectionView(View):

    def get(self, request, user):
        sections = SM(Storage()).view({})
        user_sections = []

        user = UM(Storage()).view({'username': user})
        
        for s in sections:
            if (s.get('instructor') == user[0].get('username')):
                user_sections.append(s)
        return render(request,"assign/sections.html",{'sections': sections,'user':user, 'user_sections':user_sections})

    def post(self, request, user):
        section_req = request.POST['section_select']
        split_sec = section_req.split('-')
        dept=split_sec[0]
        cnum=split_sec[1]
        snum=split_sec[2].split(' ')[0]

        section = Storage.get_section(dept=dept,cnum=cnum,snum=snum)

        fields = {'dept':dept,'cnum':cnum,'snum':snum,'instructor':user,'stype':section.stype}
        res = SM(Storage()).edit(fields)

        sections = SM(Storage()).view({})
        user = UM(Storage()).view({'username': user})
        user_sections = []

        for s in sections:
            if (s.get('instructor') == user[0].get('username')):
                user_sections.append(s)

        return render(request,"assign/sections.html",{'sections': sections,'user':user, 'user_sections':user_sections})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def About(request):
    return render(request, "main/about.html")

def FAQ(request):
    return render(request, "main/FAQ.html")

def error_404(request):
    data = {}
    return render(request, '404.html', data)

def error_500(request):
    data = {}
    return render(request, '500.html', data)

class Home(View):
    def get(self, request):
        return render(request, "main/index.html")
