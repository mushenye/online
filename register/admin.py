from django.contrib import admin

from register.models import Attendance, ClassDay, Enrollment, Person, Student

# Register your models here.
admin.site.register(Person)
admin.site.register(Enrollment)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(ClassDay)