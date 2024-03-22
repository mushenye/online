from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from register.choices import CATEGORY, LEVEL, MODE
from register.forms import PersonForm
from register.models import OnlinePerson, Person, Student
from user.forms import  RegistrationForm, SelfPersonForm
from user.models import Tracer


# Create your views here.
# registration form
def register(request):
    if request.method== 'POST':
         form= RegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             messages.success(request,f"Welcome {username} !! Your Account has been created  Succesfully. Log in to continue enjoying our services ")
             return redirect('login')
    else:
        form= RegistrationForm()
    return render(request,'user/register.html',{'form':form})


def userprofile(request):
    tracer=Tracer.objects.create()
      
    return render(request, "user/userprofile.html" ,{'tracer': tracer})
    

def category(request,pk):
    try:
        tracer=Tracer.objects.get(id=pk)
        if tracer:
            category = CATEGORY

            query = request.POST.get("query")
            if query == 'L':
                tracer.category=query
                tracer.save()
                return redirect( 'mode', tracer.id)
            
            elif query == 'T' or query == 'P' :
                tracer.category=query
                tracer.save()
                return redirect('my_name', tracer.id)
            
            elif query == 'M':
                tracer.category=query
                tracer.save()
                return redirect( 'home')
            else:
                return render(request, 'user/category.html', {'category':category ,'tracer':tracer })
            
    except Tracer.DoesNotExist:
        messages.warning(request, 'You have not selected Category, we could not verify who you are')
        return redirect('userprofile')
    

def mode(request, pk):
    try:
        tracer = Tracer.objects.get(id=pk)
        if tracer:
            mode = MODE  
            if request.method == 'POST':
                query = request.POST.get("query")
                if query in ['Online', 'Normal', 'SchoolBased', 'Special']:
                    tracer.mode = query
                    tracer.save()
                    return redirect('level', tracer.id)
            return render(request, 'user/mode.html', {'mode': mode, 'tracer': tracer})
    except Tracer.DoesNotExist:
        messages.warning(request, 'You have not selected mode, we could not verify who you are')
        return redirect('userprofile')  
  

def self_registration(request):
        if request.method == "POST":
            form = SelfPersonForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = SelfPersonForm()
        return render(request, 'register/addperson.html', context={"form": form})



def level (request, pk):
    try:
        tracer=Tracer.objects.get(id=pk)
        if tracer:
            level= LEVEL
            if request.method == 'POST':
                query = request.POST.get("query")
                if query in ['BK1','BK2']:
                    tracer.level=query
                    tracer.save()
                if tracer.mode != "Online":
                    return redirect("normal",tracer.id) 
                else:  
                    return redirect('my_name',tracer.id)     
            return render (request, 'user/level.html', {'level':level, 'tracer':tracer})        
    except Tracer.DoesNotExist:
            messages.warning(request, 'You have not selected level, we could not verify who you are')
            return redirect('userprofile')  




@login_required
def search_name(request, pk):
    user = request.user
    try:
        # to check if tracer object was generated 
        tracer = get_object_or_404(Tracer, id=pk)
        if tracer: 
            try:
                # check if online person exist
                online_person = OnlinePerson.objects.get(user=user)

                if online_person.person is not None:
                  
                    if online_person.person.category== "L":
                        student=Student.objects.get(person=online_person.person)
                    
                        if student.levels==tracer.level:
                            return redirect('verify_online', online_person.id)
                        else:
                            messages.warning(request, 'We did not Verify you , Please try again ')
                            return redirect('userprofile')
                    else:

                        return redirect('viewlesson',online_person.person.id) 
                      
                     
            except OnlinePerson.DoesNotExist:
                if request.method == 'POST':
                    query = request.POST.get("query", "")
                    if query and not isinstance(query, int):
                        # Perform search based on the query
                        try:
                            persons = Person.objects.filter(Q(first_name__icontains=query) | Q(other_name__icontains=query)).filter(category=tracer.category)[:1]
                            # filter person based on category in the tracer object
                            for person in persons:
                                if person is None:      
                                    messages.warning(request, 'We could not verify you, Try another search')
                                    return render(request, 'user/register_name.html')
                                if person.category != 'L':
                                    return render(request, 'user/register_name.html', {'persons': persons})
                                else:
                                    students = Student.objects.filter(person=person, mode=tracer.mode, levels=tracer.level) 
                                    if students:
                                        return render(request, 'user/register_name.html', {'students': students})
                                    else:
                                        messages.warning(request, 'We Could not Verify you , Please try again ')
                                
                            return render(request, 'user/register_name.html')
                        
                        except:
                            messages.info(request, "We can not find your search, you can try again ")
                            return redirect('userprofile')  
                    else:
                        messages.warning(request, "Empty search Not allowed, or we could not verify you")
                        return redirect('mode', tracer.id)
                else:
                    return render(request, 'user/register_name.html')
                
    except Tracer.DoesNotExist:
        messages.warning(request, 'Wrong request made. Try again!')
        return redirect('userprofile')

def delete_tracer(request,pk):
    tracer=Tracer.objects.get(id=pk)
    tracer.delete()
    return redirect('home')

def search_name_normal(request, pk):
    try:
        tracer = Tracer.objects.get(id=pk)
        if tracer:  
                if request.method == 'POST':
                    query = request.POST.get("query", "")
                    if query and not isinstance(query, int):
                        persons = Person.objects.filter(Q(first_name__icontains=query) | Q(other_name__icontains=query)).filter(category=tracer.category)[:1]
                        for person in persons:
                            students = Student.objects.filter(person=person, mode=tracer.mode, levels=tracer.level)
                            if students is None:
                                messages.warning(request, 'We Could not Verify you , Please try again ')
                                return redirect("userprofile")
                            return render(request, 'user/normal_name.html', {'students': students})
                    else:
                        messages.warning(request, "Empty search Not allowed, or we could not verify you")
                        return redirect('mode', tracer.id)
                else:
                    return render(request, 'user/normal_name.html') 
                
        return render(request, 'user/normal_name.html')
    
    except Tracer.DoesNotExist:
        messages.warning(request, 'Wrong request made. Try again!')
        return redirect('userprofile')



def verify_online(request, pk):
    online_person= get_object_or_404(OnlinePerson, id=pk)
    person= Person.objects.get(id = online_person.person.id)

    return render(request, 'user/online_detail.html' ,
                  {'online_person':online_person,
                   'person':person}
                  )



@login_required
def send_message(request, pk):
     pass
    # customer = request.user
    # product_detail=DetailProduct.objects.get(id=pk) 
    # conversation, created = Conversation.objects.get_or_create( customer= customer, product=product_detail.product)
    # seller_id=product_detail.supplier.id
    # seller = User.objects.get(pk=seller_id)
    # if request.method == 'POST':
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         content = form.cleaned_data['content']
    #         Chat.objects.create(sender=request.user, chat=conversation, content=content)
        
    # else:
    #     form = MessageForm()

    # msg = Chat.objects.filter(Q(sender=customer) | Q(chat=conversation)).order_by('-created_at')

    # return render(request, 'user/send_message.html', {
    #     'form': form, 
        
    #     'msg':msg
    #     })

