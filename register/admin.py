from django.contrib import admin

from register.models import Attendance, ClassDay, LessonSummary, LessonTopic, OnlineLearner, Person, Student

# Register your models here.
admin.site.register(Person)
# admin.site.register(Enrollment)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(ClassDay)
admin.site.register(LessonTopic)
admin.site.register(LessonSummary)
admin.site.register(OnlineLearner)