from django.db import models
from  . choices import  CATEGORY, MODE, LEVEL,CHURCH
from django.contrib.auth.models import User


class Person(models.Model):
    date_created=models.DateField(auto_now_add=True, blank=True, null=True)
    first_name =models.CharField(max_length=100)
    other_name =models.CharField(max_length=100)
    Local_church=models.CharField(choices=CHURCH, max_length=100 )
    category=models.CharField(choices=CATEGORY, max_length=100)


    
    def __str__(self):
        return f"{self.first_name} {self.other_name}"
    

class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    levels = models.CharField(choices=LEVEL, max_length=100,blank=True, null=True)
    mode=models.CharField(choices=MODE, max_length=100, blank=True, null=True)
    att_count=models.IntegerField(default=0)
    attendance_percent=models.IntegerField(default=1)
    is_enrolled=models.BooleanField(default=False)

    def __str__(self):
         return f"{self.person.first_name} {self.person.other_name}"
    

class LessonTopic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE )
    date_created =models.DateField(auto_now_add=True)
    date_edited=models.DateField(auto_now=True)
    taught_on_date=models.DateField()
    teacher=models.ForeignKey(Person, on_delete=models.CASCADE, related_name="teacher")
    topic= models.CharField(max_length=100)
    levels = models.CharField(choices=LEVEL, max_length=100)
    description=models.CharField(max_length=100)
    mode=models.CharField(choices=MODE, max_length=100, blank=True, null=True)
    is_taught= models.BooleanField(default=False)
    valid= models.BooleanField(default=True)
    date_taught = models.DateField( blank=True, null=True)


    def __str__ (self):
        return f"{self.topic} {self.taught_on_date}"


# class Enrollment(models.Model):
#     # user=models.ForeignKey(User,on_delete=models.CASCADE )
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
#     enrollment_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.person.first_name} {self.student.person.other_name} enrolled in {self.mode} classes on {self.enrollment_date}"

class ClassDay(models.Model):
    date_created = models.DateField(auto_now_add=True)
    lesson=models.ForeignKey(LessonTopic, on_delete=models.CASCADE)
    students=models.ManyToManyField(Student ,through="Attendance" )

    def __str__ (self):
        return f"{self.lesson.topic} on {self.date_created}"

 

class Attendance(models.Model):
    classday = models.ForeignKey(ClassDay, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    in_attendance=models.BooleanField(default=False)

    class Meta:
        unique_together = ('classday', 'student')

    def __str__(self):
        return f"{self.student.person.first_name} {self.student.person.other_name}"
    



class LessonSummary(models.Model):
    date_created = models.DateField(auto_now_add=True)
    lesson=models.ForeignKey(LessonTopic, on_delete=models.CASCADE)
    number_of_students=models.IntegerField()
    comment=models.TextField(max_length=200, blank=True, null=True)


    
    
class OnlinePerson(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True )
    person=models.OneToOneField(Person, on_delete=models.CASCADE)

    class Meta:
        unique_together=('user','person')





class Notice(models.Model):

    date_created = models.DateField(auto_now_add=True,  blank=True, null=True)
    title=models.CharField(max_length=50,blank=True, null=True)
    description=models.TextField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.title


class OnlineLesson(models.Model):
    lesson = models.ForeignKey(LessonTopic, on_delete=models.CASCADE)
    video_url = models.URLField( blank=True, null=True)  

    def __str__(self):
        return self.lesson.topic


class EnrolledStudent(models.Model):
    lesson = models.ForeignKey(OnlineLesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'student')

    def __str__(self):
        return f"{self.student.person} - {self.lesson.title}"