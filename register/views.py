from datetime import date, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from register.forms import CommentForm, LessonForm, OnlineLessonForm, PersonForm, StudentForm
from register.models import Attendance, ClassDay, LessonSummary, LessonTopic, OnlineLesson, Person, Student

# Create your views here.
def home(request):
    persons = Person.objects.all()
    query = request.POST.get("query")
    if query:
        persons = persons.filter(category=query)

    return render(request, "register/home.html", context={"persons": persons})


# def search (request):
#     if request.method == "POST":
#         query = request.POST.get("query")
#         persons = Person.objects.filter(first_name__icontains=query)  # Assuming you want to filter by first name
#         return render(request, "register/home.html", context={"persons": persons})
#     else:
#         persons = Person.objects.all()  # If it's a GET request, return all persons
#         return render(request, "register/home.html", context={"persons": persons})

def person_details(request, pk):
    person = get_object_or_404(Person, id=pk)
    context = {'person': person}

    if person.category == 'L':
        try:
            student = Student.objects.get(person=person)
            context['student'] = student
        except Student.DoesNotExist:
            pass

    return render(request, 'register/person_detail.html', context)


def add_person(request):
    user= request.user
    if user.is_staff:
        if request.method == "POST":
            form = PersonForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                if category == 'L':
                    person = form.save()
                    new_student = Student.objects.create(person=person)
                    return redirect('edit_student', new_student.id)
                else:
                    form.save()
                    return redirect('home')  
        else:
            form = PersonForm()
        return render(request, 'register/addperson.html', context={"form": form})
    else:
        messages.warning(request, 'Request not allowed !!')
        return redirect('home')


def edit_person(request, pk):

    try: 
        person = get_object_or_404(Person, id=pk)
    except Person.DoesNotExist:
       
        messages.warning(request, "No person found. Check your credentials.")
        return redirect('home')

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            category = form.cleaned_data['category']
            if category == 'L':
                person = form.save() 
                new_student, created = Student.objects.get_or_create(person=person)
                return redirect('edit_student', new_student.id)
            else:
                form.save()
                try:
                    student = Student.objects.get(person=person)
                    student.delete()
                except Student.DoesNotExist:
                    pass  
                return redirect('home')
    else:
        form = PersonForm(instance=person)
    
    return render(request, 'register/addperson.html', context={"form": form})

         
       

def student(request,pk):
    student=Student.objects.get(id=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)
        # persons = Person.objects.filter(category="L")
      
        # form.fields['person'].queryset = persons

    return render(request, 'register/addperson.html', context={"form": form})




def lessons (request):
    user=request.user
    if user:
        if request.method == "POST":
            form = LessonForm(request.POST, initial={'user':user})
            if form.is_valid():
                mode =form.cleaned_data['mode']
                if mode =='Online':
                    lesson=form.save()

                    onlinelesson, created =OnlineLesson.objects.get_or_create(lesson=lesson)
                    return redirect("onlinelesson", onlinelesson.id )
                else:

                    form.save( )
            return redirect('viewlesson')
        else:
            form = LessonForm(initial={'user':user})
            persons = Person.objects.filter(category="T")
            form.fields['teacher'].queryset = persons
    else:
        return redirect('login')  
    
    return render(request, 'register/lesson.html', {'form': form})





def onlineclass(request,pk):
    onlinelesson= OnlineLesson.objects.get(id=pk)
    if request.method =="POST":
        form = OnlineLessonForm(request.POST, instance=onlinelesson)
        if form.is_valid():
            form.save()
            return redirect('viewlesson')
    else:
        form = OnlineLessonForm(instance=onlinelesson)
    return render(request, 'register/onlineform.html', {'form':form})


def lesson_edit(request, pk):
    user=request.user
    if user.is_staff:
        try: 
            lesson = get_object_or_404(LessonTopic, id=pk)
        except Person.DoesNotExist:
            messages.warning(request, "No such lesson exits.")
            return redirect('viewlesson')
        if lesson.is_taught== False:
            if request.method == "POST":
                form = LessonForm(request.POST, instance=lesson)
                if form.is_valid():
                    mode= form.cleaned_data['mode']
                    if mode== 'Online':
                        form.save()
                        onlinelesson, created= OnlineLesson.objects.get_or_create(lesson=lesson)
                        return redirect("onlinelesson", onlinelesson.id )
                    else:
                        form.save()
                        try:
                            onlinelesson = OnlineLesson.objects.get(lesson=lesson)
                            onlinelesson.delete()
                        except OnlineLesson.DoesNotExist:
                            pass 
                        return redirect('viewlesson')
            else:
                form = LessonForm(instance=lesson)
                persons = Person.objects.filter(category="T")
                form.fields['teacher'].queryset = persons
        else:
            messages.warning(request,'This lesson is already taught, add another lesson to continue')

        return render(request, 'register/lesson.html', {'form': form})
    else:
        messages.warning(request,'You are not allowed to edit')
        return redirect( 'viewlesson')


def view_lessons(request):
    lessons = LessonTopic.objects.all().order_by("-date_created")
    today_date = date.today()
    
    valid_lessons = [lesson for lesson in lessons if lesson.taught_on_date < today_date]

    LessonTopic.objects.filter(id__in=[lesson.id for lesson in valid_lessons]).update(valid=False)

    return render(request, 'register/lesson_view.html', {'lessons': lessons})



def view_lesson(request, pk):
    lesson = LessonTopic.objects.get(id=pk)
    classday, created = ClassDay.objects.get_or_create(lesson=lesson)
    
    if created:
        students = Student.objects.filter(levels=lesson.levels, mode=lesson.mode)
        if students.exists():
            for student in students:
                Attendance.objects.create(classday=classday, students=student)
        else:
            return redirect("viewlesson")
        
    attendance = Attendance.objects.filter(classday=classday)
    # if attendance.filter(in_attendance=True):
    #     lesson.is_taught=True
    #     lesson.save()
    return render(request, 'register/lesson_detail.html', {'lesson': lesson, 'attendance': attendance})





def mark_attendance(request, pk):
    attendance = get_object_or_404(Attendance, id=pk)
    if attendance.classday.lesson.valid == True:
        if attendance.in_attendance == False:
            attendance.in_attendance = True
            attendance.save()

            try:
                student = attendance.students
                student.att_count += 1  
                student.save()
            except Student.DoesNotExist:
                pass

        else:
            attendance.in_attendance = False
            attendance.save()

            try:
                student = attendance.students
                student.att_count -= 1  
                student.save()
            except Student.DoesNotExist:
                pass
    else:
        messages.warning(request, "You can not be able to mark the attendance,")
    return redirect('details', attendance.classday.lesson.id)


def close_lesson(request, pk):
    lesson = get_object_or_404(LessonTopic, id=pk)
    classday = ClassDay.objects.get(lesson=lesson)
    student_count = classday.students.count()
    lesson_summary, created = LessonSummary.objects.get_or_create(lesson=lesson, number_of_students=student_count)
   
    if created:

        lesson=LessonTopic.objects.get(id=lesson_summary.lesson.id)

        lesson.is_taught=True
        lesson.valid =False
        lesson.save()
        
        return redirect('comment', lesson_summary.id)

    else:
        return redirect('viewlesson')




def comment(request, pk):
    lessonsummary = get_object_or_404(LessonSummary, id=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=lessonsummary)
        if form.is_valid():
            form.save()
            return redirect('viewlesson')  
    else:
        form = CommentForm(instance=lessonsummary)
    
    return render(request, 'register/comment.html', {'form': form})





def enrol_learner(request, pk):
    lesson = LessonTopic.objects.get(id=pk)
    classday=get_object_or_404(ClassDay, lesson=lesson)
    students=Student.objects.filter(levels=lesson.levels, mode=lesson.mode)
  
    if students:
        
        for student in students:
            Attendance.objects.get_or_create(classday=classday, students=student)
                              
    else:
        messages.warning(request, "Check if the learner's details have been added correctly")

    return redirect("details", lesson.id)


def report(request):
    report = ClassDay.objects.filter(attendance__in_attendance=False)

    return render(request, 'register/report.html', {'report': report})


def student_attendance(request,pk):
    student=get_object_or_404(Student, id=pk)
    attendance=Attendance.objects.filter(in_attendance=True, students=student).count
    
    return render(request, 'register/report2.html', {'attendance': attendance})



def attendance_summary(request):
    class_days = ClassDay.objects.all().prefetch_related('attendance_set')
    return render(request, 'register/attendance_summury.html', {'class_days': class_days})




def view_video(request, pk):
    lesson = get_object_or_404(LessonTopic, id=pk)
    video_url = None
    try:
        online_lesson = OnlineLesson.objects.get(lesson=lesson)
        video_url = online_lesson.video_url 
    except OnlineLesson.DoesNotExist:
        pass

    return render(request, 'register/video.html', {'video_url': video_url})