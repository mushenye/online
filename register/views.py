from datetime import date, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from register.forms import AttendaceForm, CommentForm, LessonForm, OnlineLessonForm, PersonForm, StudentForm
from register.models import Attendance, ClassDay, LessonSummary, LessonTopic, OnlineLearner, OnlineLesson, Person, Student

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

                if new_student.mode != 'Online':
                   return redirect('learner_enrol', student.id)
                else:
                    OnlineLearner.objects.create(person=student.person)

                return redirect('home')
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

def onlineclass(request,pk):
    user=request.user
    if user.is_staff:
        onlinelesson= OnlineLesson.objects.get(id=pk)
        if request.method =="POST":
            form = OnlineLessonForm(request.POST, instance=onlinelesson)
            if form.is_valid():
                form.save()
                return redirect('viewlesson')
        else:
            form = OnlineLessonForm(instance=onlinelesson)

        return render(request, 'register/onlineform.html', {'form':form})
    else:
        messages.warning(request, 'Request not allowed !!')
        return redirect('home')
    


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
    user=request.user
    attendance = get_object_or_404(Attendance, id=pk)
    if attendance.classday.lesson.user == user:
        if attendance.student.mode  != 'Online':
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
    report = ClassDay.objects.filter(attendance__in_attendance=False)

    return render(request, 'register/report.html', {'report': report})


def student_attendance(request,pk):
    student=get_object_or_404(Student, id=pk)
    attendance=Attendance.objects.filter(in_attendance=True, students=student).count
    
    return render(request, 'register/report2.html', {'attendance': attendance})



def attendance_summary(request):
    class_days = ClassDay.objects.all().prefetch_related('attendance_set')
    return render(request, 'register/attendance_summury.html', {'class_days': class_days})


def register_online(request, pk):
    user=request.user
    
    if user.is_authenticated:
        try:
            
            person=Person.objects.get(id=pk)
            OnlineLearner.objects.get(user=user, person=person)

            if person:
                try:
                    online_learner= get_object_or_404(OnlineLearner, person=person)
                    online_learner.user=user
                    online_learner.save()

                    student=Student.objects.get(person=person)
                    student.is_enrolled= True
                    student.save()


                    messages.success(request, f'Welcome back ( {user}, Name: {person}) select Lesson to continue')
                    return redirect('viewlesson') 


                except OnlineLearner.DoesNotExist:
                    messages.warning(request, 'Please register for online classes with credentials')
                    return redirect('register_person')
            else:
                messages.warning(request," Person is not registerd for online classes" )
            
        except OnlineLearner.DoesNotExist:
            messages.warning(request,f" User not allowed to use {person}, you are logged in as {user}. if you are Online Learner login with your credentials"  )
   
    return redirect('home')


def join_online(request, pk):
    user = request.user

    if user.is_authenticated:
        lesson = get_object_or_404(LessonTopic, id=pk)
        classday = get_object_or_404(ClassDay, lesson=lesson)
        online = get_object_or_404(OnlineLesson, lesson=lesson)
        try:
            online_learner = OnlineLearner.objects.get(user=user)
            student=Student.objects.get(person=online_learner.person)
            attendance = get_object_or_404(Attendance, classday=classday, student= student)
            if attendance.classday.lesson.valid and not attendance.in_attendance:
                attendance.in_attendance = True
                attendance.save()
                try:
                    student = attendance.student
                    student.att_count += 1  
                    student.save()
                except Student.DoesNotExist:
                    pass
            return redirect('videoview', online.id)
        except OnlineLearner.DoesNotExist:
            return redirect('viewlesson' )
    else:
        messages.warning(request, 'Yo are not authenticated, Please log in to continue')
        return redirect('login')






# def online_attendance(request, pk):
#     user=request.user
#     lesson = get_object_or_404(LessonTopic, id=pk)
#     classday = get_object_or_404(ClassDay, lesson=lesson)
#     if request.method == "POST":
#         form = AttendaceForm(request.POST, initial={"classday": classday})
#         if form.is_valid():
#             person = form.cleaned_data['person']
            
#             form.save()
#             OnlineLearner.objects.create(user=request.user, person=person)
#             return redirect('join_online', lesson.id)
#         else:
#             messages.warning(request, 'Invalid response, please consult your administrator')
#             return redirect('viewlesson')
#     else:
#         form = AttendaceForm(initial={"classday": classday})
#         students = Student.objects.filter(mode="Online")
#         if students:
#             form.fields['students'].queryset = students
#         else:
#             messages.info(request, 'No online student has been registered')
#             return redirect('register_person')
#         return render(request, 'register/join_online.html', {'form': form})

    


def view_video(request, pk):
    lesson = get_object_or_404(LessonTopic, id=pk)
    video_url = None
    try:
        online_lesson = OnlineLesson.objects.get(lesson=lesson)
        video_url = online_lesson.video_url 
    except OnlineLesson.DoesNotExist:
        pass

    return render(request, 'register/video.html', {'video_url': video_url})