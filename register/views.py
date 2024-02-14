import datetime
from django.shortcuts import get_object_or_404, redirect, render

from register.forms import LessonForm, PersonForm, StudentForm
from register.models import Attendance, ClassDay, LessonTopic, Person, Student

# Create your views here.
def home(request):
    persons =Person.objects.all()
    return render(request, "register/home.html" , context=
                  {"persons":persons} )


def add_person(request):
    if request.method == "POST":
        form=PersonForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form=PersonForm()
    return render(request,'register/addperson.html',
                 context={"form":form} )

def student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
        persons = Person.objects.filter(category="L")
      
        form.fields['person'].queryset = persons

    return render(request, 'register/student.html', {'form': form})



def lessons (request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
          lesson =  form.save()

        return redirect('home')
    else:
        form = LessonForm()
        persons = Person.objects.filter(category="T")
        form.fields['teacher'].queryset = persons
      
    return render(request, 'register/lesson.html', {'form': form})


def view_lessons(request):
    lesson=LessonTopic.objects.all()
    return render(request, 'register/lesson_view.html', context={'lesson':lesson})

def view_lesson(request, pk):
    lesson = LessonTopic.objects.get(id=pk)
    classday, created = ClassDay.objects.get_or_create(lesson=lesson)
    
    if created:
        # If a new ClassDay was created, create attendance records for all associated students
        students = Student.objects.filter(levels=lesson.levels)
        for student in students:
            Attendance.objects.create(classday=classday, student=student)

    return render(request, 'register/lesson_detail.html', {'lesson': lesson})


def View_attendance(request):
    attendance= Attendance.objects.all().filter(in_attendance=False)
    return render(request, 'register/view_attendance.html', context={
        'attendance':attendance
    })



def mark_attendance(request, pk):
    attendance = get_object_or_404(Attendance, id=pk) 
    attendance.in_attendance = True
    attendance.save()  
    return redirect('view_attendance')




def attendance_summary(request):
    class_days = ClassDay.objects.all().prefetch_related('attendance_set')
    return render(request, 'register/attendance_summury.html', {'class_days': class_days})