from django.contrib import admin
from .models import Course, Staff, Section

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Staff)
# Register your models here.