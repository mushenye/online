from datetime import date, datetime, timedelta
from django.db.models import Q

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from register.forms import AttendaceForm, CommentForm, LessonForm, NoticeForm, OnlineLessonForm, PersonForm, StudentForm
from register.models import Attendance, ClassDay, LessonSummary, LessonTopic, Notice, OnlinePerson, OnlineLesson, Person, Student

# Create your views here.

def index(request):
    user = request.user
    context = {'person': None}
    query_search = request.POST.get("query", "")

    if query_search:
        persons = Person.objects.filter(Q(first_name__icontains=query_search) | Q(other_name__icontains=query_search))[:2]
        lessons = LessonTopic.objects.filter(Q(topic__icontains=query_search) | Q(description__icontains=query_search))[:2]

    
        context['persons'] = persons
        context['lessons'] = lessons

    if user.is_authenticated:
        try:
            onlineperson = OnlinePerson.objects.get(user=user)
            context['person'] = onlineperson.person
        except OnlinePerson.DoesNotExist:
            messages.info(request, "We could not verify who you are")
            return redirect('userprofile')

    return render(request, 'register/index.html', context)

    

 
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "register/learner_list.html", context={
        "students": students,
        "page_obj": page_obj
        })




def members(request):
    person = Person.objects.exclude(category='L')
    paginator = Paginator(person, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "register/members.html", context={"page_obj": page_obj})



def person_details(request, pk):
    person = get_object_or_404(Person, id=pk)
    context = {'person': person}

    if person.category == 'L':
        try:
            student = Student.objects.get(person=person)
            context['student'] = student
        
        except Student.DoesNotExist:
            pass

    return render(request, 'register/learner_detail.html', context)



@login_required
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
                elif category == 'T' or category == 'P':
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
    


@login_required
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
        try:
            onlineperson=OnlinePerson.objects.get(user=user)

            if request.method == "POST":
                form = LessonForm(request.POST, initial={'user':user})
                if form.is_valid():
                    mode =form.cleaned_data['mode']
                    if mode =='Online':
                        lesson=form.save()
                        onlinelesson, created =OnlineLesson.objects.get_or_create(lesson=lesson)
                        return redirect("onlinelesson", onlinelesson.id )
                    else:
                        form.save()

                return redirect('viewlesson', onlineperson.person.id)
            else:
                form = LessonForm(initial={'user':user})
        
                return render(request, 'register/lesson.html', {'form': form})
        except OnlinePerson.DoesNotExist:
            messages.wrning(request, "You may be unauthorised to add lesson, try again")
            return redirect('userprofile')
    else:
        return redirect('login')  

    


def lesson_edit(request, pk):
    user=request.user
    if user.is_staff:
        try:
            onlineperson=OnlinePerson.objects.get(user=user)
            try: 
                lesson = LessonTopic.objects.get(id=pk) 
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
                                return redirect('viewlesson',onlineperson.person.id )
                    else:
                        form = LessonForm(instance=lesson)
                        return render(request, 'register/lesson.html', {'form': form})     
                else:
                    messages.warning(request,'This lesson is already taught, add another lesson to continue')
                    return redirect('addlesson')       

            except LessonTopic.DoesNotExist:
                messages.warning(request, "No such lesson exits.")
                return redirect('home' )
        except OnlinePerson.DoesNotExist:
            messages.warning(request, 'You are not validated to person that functions')
            return redirect('home')  
    else:
        messages.warning(request,'You are not allowed to edit')
        return redirect( 'home')
    


def enroll(request, pk):
    user= request.user
    if user.is_staff:
        student=get_object_or_404(Student, id=pk)
        student.is_enrolled= True
        student.save()
        messages.success(request, f'{student.person} has been enrolled in {student.mode} class succesfully')
    else:
        messages.warning(request, 'Request not allowed !!')
    return redirect('userprofile')


# adding  lesson form 
def online_class(request, pk):
    online=OnlineLesson.objects.get(id=pk)
    if request.method == 'POST':
        form=OnlineLessonForm(request.POST,instance=online)
        if form.is_valid():
            form.save()
            return redirect ('home')
    else:
        form=OnlineLessonForm(instance=online)
    return render(request, 'register/onlineform.html', {'form':form})

 


 #view lesson 
def view_lessons(request, pk):
    person=Person.objects.get(id=pk)
    lessons = LessonTopic.objects.all().order_by("-date_created")
    today_date = date.today()

    query = request.POST.get("query")


    if person.category != "L":
        
        valid_lesson = [lesson for lesson in lessons if lesson.taught_on_date < today_date]
        LessonTopic.objects.filter(id__in=[lesson.id for lesson in valid_lesson]).update(valid=False)
        if query:
            if query == "next":
                lessons=lessons.filter(taught_on_date__gte=today_date)[:4]
            elif query == "today":
                lessons=lessons.filter(taught_on_date = today_date)
            else:
                lessons=lessons

    else:
        student =Student.objects.get (person=person)
        lessons = lessons.filter( levels=student.levels, mode =student.mode )
        valid_lessons = [lesson for lesson in lessons if lesson.taught_on_date < today_date]
        LessonTopic.objects.filter(id__in=[lesson.id for lesson in valid_lessons]).update(valid=False)
        if query:
            if query == "next":
                lessons=lessons.filter(taught_on_date__gte=today_date)[:2]
            elif query == "today":
                lessons=lessons.filter(taught_on_date = today_date)
            else:
                lessons=lessons
            
    paginator = Paginator(lessons, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  


    return render(request, 'register/lesson_view.html', {'lessons': lessons,'page_obj':page_obj})


def view_lesson(request, pk):
    user=request.user
    onlineperson=OnlinePerson.objects.get(user=user)

    lesson = LessonTopic.objects.get(id=pk)

    classday, created = ClassDay.objects.get_or_create(lesson=lesson)
    
    if created:
        students = Student.objects.filter(levels=lesson.levels, mode=lesson.mode)
        if students.exists():
            for student in students:
                Attendance.objects.create(classday=classday, student=student)
                    
       
        
    class_attendance = Attendance.objects.filter(classday=classday)

    paginator = Paginator(class_attendance, 4)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
  
    return render(request, 'register/lesson_detail.html', {'lesson': lesson, 'class_attendance': class_attendance, 'page_obj':page_obj, 'onlineperson':onlineperson})


# def today_lesson(request):
#     today_date=today_date = date.today()
#     lessons=LessonTopic.objects.filter(taught_on_date=today_date, valid=True)

#     return render(request, 'register/lesson_view.html', {'lessons': lessons})





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
        return redirect('viewlesson', lesson.user.person.id )
    

def lesson_summary(request):
    
    lesson=LessonSummary.objects.all()
    
    return render(request, 'register/lesson_summary.html' ,context={
        'lesson':lesson
    })


def comment(request, pk):
    user=request.user
    lessonsummary = get_object_or_404(LessonSummary, id=pk)
    onlineperson=OnlinePerson.objects.get(user=user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=lessonsummary)
        if form.is_valid():
            form.save()
            return redirect('viewlesson', onlineperson.person.id)  
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






def register_online(request, pk):
    user=request.user
    if user.is_authenticated:

        person=Person.objects.get(id=pk)
        try:
            learner= OnlinePerson.objects.get(person=person) 
            if learner.user == user:
                messages.success(request, f'Welcome back ( {user}, Name: {person}) select Lesson to continue')
                return redirect('viewlesson', person.id)

            else:
                learner.user=user
                learner.save()

                student=Student.objects.get(person=person)
                student.is_enrolled= True
                student.save()
                return redirect('viewlesson', person.id)
            
        except:
            messages.warning(request, f' You can Not log in with  ( {user}, and  {person}) for online class')
            return redirect ('userprofile') 
    
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
            
            try:
                attendance = Attendance.objects.get(classday=classday, student= student) 
            except Attendance.DoesNotExist:
                return redirect('enrol',lesson.id)

            if attendance.classday.lesson.valid and not attendance.in_attendance:
                lesson_count=LessonTopic.objects.filter(levels=attendance.student.levels,  mode=attendance.student.mode).count()

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
            return redirect('viewlesson', lesson.user.person.id)
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




