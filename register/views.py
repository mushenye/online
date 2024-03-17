from datetime import date, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from register.forms import AttendaceForm, CommentForm, LessonForm, NoticeForm, OnlineLessonForm, PersonForm, StudentForm
from register.models import Attendance, ClassDay, LessonSummary, LessonTopic, Notice, OnlinePerson, OnlineLesson, Person, Student

# Create your views here.

def index(request):

    return render(request, 'register/index.html')


def person_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "register/home.html", context={
        "students": students,
        "page_obj": page_obj
        })


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


def enroll(request, pk):
    user= request.user
    if user.is_staff:
        student=get_object_or_404(Student, id=pk)
        student.is_enrolled= True
        student.save()
        messages.success(request, f'{student.person} has been enrolled in {student.mode} class succesfully')

    else:
        messages.warning(request, 'Request not allowed !!')

    return redirect('home')


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
                elif category == 'T':
                    person = form.save()
                    OnlinePerson.objects.create(person=person)
                    return redirect('home')
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
    user=request.user
    if user.is_staff:
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
                
                elif category == 'T':
                    person = form.save()
                    OnlinePerson.objects.get_or_create(person=person)
                    return redirect('home')
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
    else:
        messages.warning(request, 'Request not allowed !!')
        return redirect('home')
         
       

def student(request,pk):
    user=request.user
    if user.is_staff:
        student=Student.objects.get(id=pk)
        if request.method == "POST":
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                new_student=form.save()
                try:

                    if new_student.mode != 'Online':
                        online_learner =get_object_or_404(OnlinePerson, person=student.person)
                        online_learner.delete()
                        return redirect('learner_enrol', student.id)
                    else: 
                        OnlinePerson.objects.create(person=student.person) 
                        return redirect('home')
                except:
                    return redirect('learner_enrol', student.id)
        else:
            form = StudentForm(instance=student)

        return render(request, 'register/addperson.html', context={"form": form})
    else:
        messages.warning(request, 'Request not allowed !!')
        return redirect('home')



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
            if persons:
                    form.fields['teacher'].queryset = persons

            else:
                    messages.info(request,'No teacher exist. You can register ')
                    return redirect('register_person')        
    else:
        return redirect('login')  
    return render(request, 'register/lesson.html', {'form': form})



#form to register new student as online

# def onlineclass(request,pk):
#     user=request.user
#     if user.is_staff:
#         onlinelesson= OnlineLesson.objects.get(id=pk)
#         if request.method =="POST":
#             form = OnlineLessonForm(request.POST, instance=onlinelesson)
#             if form.is_valid():
#                 lesson=form.save()
#                 return redirect('details',lesson.id )
#         else:
#             form = OnlineLessonForm(instance=onlinelesson)

#         return render(request, 'register/onlineform.html', {'form':form})
#     else:
#         messages.warning(request, 'Request not allowed !!')
#         return redirect('home')
    


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
                    lesson= form.save(commit=False)
                    if mode== 'Online':
                        lesson.valid= True
                        lesson.is_taught =False
                        form.save()
                    
                        onlinelesson, created= OnlineLesson.objects.get_or_create(lesson=lesson)
                        return redirect("onlinelesson", onlinelesson.id )
                    else:
                        lesson.valid= True
                        lesson.is_taught =False
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
                if persons:
                    form.fields['teacher'].queryset = persons
                else:
                    messages.info(request,'No teacher exist')
                    return redirect('register_person')
        else:
            messages.warning(request,'This lesson is already taught, add another lesson to continue')

        return render(request, 'register/lesson.html', {'form': form})
    else:
        messages.warning(request,'You are not allowed to edit')
        return redirect( 'viewlesson')


def view_lessons(request, pk):
    person=Person.objects.get(id=pk)
    today_date = date.today()
    if person.category != "L":

        lessons = LessonTopic.objects.all().order_by("-date_created")
        valid_lesson = [lesson for lesson in lessons if lesson.taught_on_date < today_date]
        LessonTopic.objects.filter(id__in=[lesson.id for lesson in valid_lesson]).update(valid=False)

    else:
        student =Student.objects.get (person=person)
        lessons = LessonTopic.objects.filter( levels=student.levels, mode =student.mode ).order_by("-date_created")
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
                Attendance.objects.create(classday=classday, student=student)
        else:
            return redirect("viewlesson")
        
    class_attendance = Attendance.objects.filter(classday=classday)
  
    return render(request, 'register/lesson_detail.html', {'lesson': lesson, 'class_attendance': class_attendance})





def mark_attendance(request, pk):
    user=request.user
    attendance = get_object_or_404(Attendance, id=pk)
    if attendance.classday.lesson.user == user:
        if attendance.student.mode  != 'Online':
            lesson=LessonTopic.objects.filter(levels=attendance.student.levels,  mode=attendance.student.mode).count()

            if attendance.classday.lesson.valid == True:
                if attendance.in_attendance == False:
                    attendance.in_attendance = True
                    attendance.save()

                    try:
                        student = attendance.student
                        student.att_count += 1
                        student.attendance_percent=( student.att_count/lesson * 100)
                        student.save()
                    except Student.DoesNotExist:
                        pass

                else:
                    attendance.in_attendance = False
                    attendance.save()

                    try:
                        student = attendance.student
                        student.att_count -= 1 
                        student.attendance_percent=( student.att_count/lesson * 100)
                        student.save()
                    except Student.DoesNotExist:
                        pass
            else:
                messages.warning(request, "You can not be able to mark the attendance,")
        else:
            messages.warning(request, "You cannot be able to Mark attendance for online class. The learner MUST be loged in with his/her credentials")
   
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
        lesson.date_taught= datetime.now()
        lesson.save()

        return redirect('comment', lesson_summary.id)

    else:
        return redirect('viewlesson')

def lesson_summary(request):
    
    lesson=LessonSummary.objects.all()
    
    return render(request, 'register/lesson_summary.html' ,context={
        'lesson':lesson
    })


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





def learner_in_class (request, pk):
    lesson = LessonTopic.objects.get(id=pk)
    classday=get_object_or_404(ClassDay, lesson=lesson)
    students=Student.objects.filter(levels=lesson.levels, mode=lesson.mode, is_enrolled=True)
    if students:
        for student in students:
            Attendance.objects.get_or_create(classday=classday, student=student)                
    else:
        messages.warning(request, "Check if the learner's details have been added correctly")

    return redirect("details", lesson.id)



def report(request):
    classday=ClassDay.objects.filter()

    return render(request, 'register/report.html', )




def student_attendance(request,pk):
    student=get_object_or_404(Student, id=pk)
    attendance=Attendance.objects.filter(in_attendance=True, students=student).count()
    
    return render(request, 'register/report2.html', {'attendance': attendance})



def attendance_summary(request):
    class_days = ClassDay.objects.all().prefetch_related('attendance_set')
    
    return render(request, 'register/attendance_summury.html', {'class_days': class_days})


def view_attendance(request, pk):
    class_day = get_object_or_404(ClassDay, pk=pk)
    attendance_records = class_day.attendance_set.all()

    return render(request, 'register/view_attendance.html', 
                  {'class_day': class_day, 
                   'attendance_records': attendance_records})





def register_online(request, pk):
    user=request.user
    if user.is_authenticated:
        try:
            person=Person.objects.get(id=pk)

            try:
                learner= OnlinePerson.objects.get(person=person) 
            except OnlinePerson.DoesNotExist:
                messages.warning(request, "Person  does not exist, Consult your administrator")
                return redirect('userprofile')

            if learner.user == user:
                messages.success(request, f'Welcome back ( {user}, Name: {person}) select Lesson to continue')
                return redirect('viewlesson', person.id)
            
            elif learner.user == None:
                try:
                    learner.user=user
                    learner.save()
                except:
                    messages.warning(request, ' User with this Person already exists.')
                    return redirect('userprofile')

                student=Student.objects.get(person=person)
                student.is_enrolled= True
                student.save()

                messages.success(request, f'Welcome ( {user}, Name: {person}) select Lesson to continue')
                return redirect('viewlesson', person.id)
            else:
                messages.warning(request, f' You can Not log in with  ( {user}, and  {person}) for online class')
                return redirect ('userprofile')
        except Person.DoesNotExist:
            messages.warning(request, 'We could find the person, try another search')
            return redirect('userprofile') 
    else:
        return redirect ('login')              
                   
   


def join_online(request, pk):
    user = request.user

    if user.is_authenticated:
        lesson = get_object_or_404(LessonTopic, id=pk)
        classday = get_object_or_404(ClassDay, lesson=lesson)
        online = get_object_or_404(OnlineLesson, lesson=lesson)
        try:
            online_learner = OnlinePerson.objects.get(user=user)
            student=Student.objects.get(person=online_learner.person)
            attendance = get_object_or_404(Attendance, classday=classday, student= student)
            if attendance.classday.lesson.valid and not attendance.in_attendance:
                lesson_count=LessonTopic.objects.filter(level=attendance.student.levels,  mode=attendance.student.mode).count()

                attendance.in_attendance = True
                attendance.save()
                try:
                    student = attendance.student
                    student.att_count += 1  
                    student.attendance_percent=( student.att_count/lesson_count * 100)
                    student.save()
                except Student.DoesNotExist:
                    pass
            return redirect('videoview', online.id)
        except OnlinePerson.DoesNotExist:
            messages.warning(request, 'Leaner does not Exist')
            return redirect('viewlesson' )
    else:
        messages.warning(request, 'Yo are not authenticated, Please log in to continue')
        return redirect('login')




    


def view_video(request, pk):
    lesson = get_object_or_404(LessonTopic, id=pk)
    video_url = None
    try:
        online_lesson = OnlineLesson.objects.get(lesson=lesson)
        video_url = online_lesson.video_url 
    except OnlineLesson.DoesNotExist:
        pass

    return render(request, 'register/video.html', {'video_url': video_url})


# function to add notices 

def create_notice(request):
    form=NoticeForm()
    if request.method=="POST":
        form=NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view')
    context={
        'form':form
    }

    return render(request, 'register/notice.html', context)



def notice_view(request):
    notices=Notice.objects.all().order_by('-date_created')
    context={
        'notices':notices
    }

    return render(request, 'register/notice_view.html', context)


def notice_update(request, pk):
    notice=Notice.objects.get(id=pk)
    form=NoticeForm(instance=notice)
    if request.method=="POST":
        form=NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('view')
        
    context={
        'form':form
    }
    return render(request, 'register/notice.html', context)



def notice_delete(request,pk):
    notice=Notice.objects.get(id=pk)
    notice.delete()
    return redirect('view')




