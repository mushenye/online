from django.db import models
from choices  import  CATEGORY, MODE, LEVEL

class Person(models.Model):
    first_name =models.CharField(max_length=100)
    other_name =models.CharField(max_length=100)
    email = models.EmailField()
    category=models.CharField(choices=CATEGORY, max_length=100)

    def name(self):
        return "{} {}" .format(self.first_name,self.other_name)
    
    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    levels = models.CharField(LEVEL, through='Enrollment')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mode=models.CharField(choices=MODE, max_length=100)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} enrolled in {self.mode} on {self.enrollment_date}"

 

class Attendance(models.Model):
  
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    in_attendance=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date}: {self.status}"
