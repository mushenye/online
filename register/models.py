from django.db import models
from  . choices import  CATEGORY, MODE, LEVEL,CHURCH
from django.contrib.auth.models import User


class Person(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE )
    first_name =models.CharField(max_length=100)
    other_name =models.CharField(max_length=100)
    Local_church=models.CharField(choices=CHURCH, max_length=100 )
    category=models.CharField(choices=CATEGORY, max_length=100)

 
    
    def __str__(self):
        return f"{self.first_name} {self.other_name}"
    

class Student(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    levels = models.CharField(choices=LEVEL, max_length=100)

    def __str__(self):
         return f"{self.person.first_name} {self.person.other_name}"
    

class LessonTopic(models.Model):
    date_created =models.DateField(auto_now_add=True)
    date_edited=models.DateField(auto_now=True)
    date=models.DateField()
    teacher=models.ForeignKey(Person, on_delete=models.CASCADE)
    topic= models.CharField(max_length=100)
    levels = models.CharField(choices=LEVEL, max_length=100)
    description=models.CharField(max_length=100)

    def __str__ (self):

        return f"{self.topic} {self.date}"


class Enrollment(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mode=models.CharField(choices=MODE, max_length=100)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.person.first_name} {self.student.person.other_name} enrolled in {self.mode} classes on {self.enrollment_date}"

class ClassDay(models.Model):
    date_created = models.DateField(auto_now_add=True)
    lesson=models.ForeignKey(LessonTopic, on_delete=models.CASCADE)
    students=models.ManyToManyField(Student ,through="Attendance" )

    def __str__ (self):
        return f"{self.lesson.topic} on {self.date_created}"
 

class Attendance(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE )
    classday = models.ForeignKey(ClassDay, on_delete=models.CASCADE)
    students=models.ForeignKey(Student, on_delete=models.CASCADE)
    in_attendance=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.students.person.first_name} {self.students.person.other_name}"
    

class Notice (models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()

    

# class Lesson (models.Model):
#     date= models.DateField(auto_now_add=True)
#     teacher= models.ForeignKey(Person, on_delete=models.CASCADE)
#     learner= models.ManyToManyField( Attendance, through="DayLesson")

# class DayLesson(models.Model):
#     lesson =models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     attendance= models.ForeignKey(Attendance, on_delete=models.CASCADE)
