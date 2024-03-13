from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from register.choices import CATEGORY, LEVEL, MODE
from register.models import OnlineLearner, Person
from user.forms import  RegistrationForm
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
      
    return render(request, "user/userprofile.html")
    

def category(request,Pk):
    try:
        tracer=Tracer.objects.get(id=Pk)
        if tracer:
            category = CATEGORY

            query = request.POST.get("query")
            if query == 'L':
                mode= MODE
                tracer.mode=query
                tracer.save()
                return redirect( 'mode', tracer.id)
            
            elif query == 'T':
                tracer.mode=query
                tracer.save()
                return redirect('home')
            elif query == 'P':
                tracer.mode=query
                tracer.save()
                return redirect('home')
            elif query == 'M':
                tracer.mode=query
                tracer.save()
                return redirect( 'home')
            else:
                return render(request, 'user/category.html', {'category':category })
    except Tracer.DoesNotExist:
        messages.warning(request, 'You have not selected')
        return redirect('userprofile')
    

def mode(request, pk):
    try:
        tracer=Tracer.objects.get(id=pk)
        if tracer:
            mode= MODE
            query = request.POST.get("query")
            if query == 'Online':
                    tracer.mode=query
                    tracer.save()
                    return redirect( 'my_name',tracer.id)
            elif query == 'Normal':
                    return redirect('viewlesson')
            elif query == 'SchoolBased':
                    return redirect('')
            elif query == 'Special':
                return redirect( 'home')
            else:
                return render(request, 'user/mode.html', {'mode':mode})
    except Tracer.DoesNotExist:
        messages.warning(request, 'You have not selected')
        return redirect('userprofile')   
    

def level (request, pk):
    try:
        tracer=Tracer.objects.get(id=pk)
        if tracer:
            level= LEVEL
            query = request.POST.get("query")
            if query == 'BK1':
                tracer.level=query
                return redirect()
            else:
                return redirect()

        return render ()

    except Tracer.DoesNotExist:
            messages.warning(request, 'You have not selected')
            return redirect('userprofile')  


@login_required
def search_name(request):
    user = request.user

    try:
        online_learner = OnlineLearner.objects.get(user=user)
        if online_learner.person is not None:
            return redirect('verify_online', online_learner.id)
        else:
            messages.warning(request, "Try to search by your name")
            return render(request, 'user/register_name.html')
    except OnlineLearner.DoesNotExist:
        messages.warning(request, "Online learner object does not exist for this user") 

        if request.method == 'POST':
            query = request.POST.get("query", "")
            
            if query:
                # Perform search based on the query
                persons = Person.objects.filter(Q(first_name__icontains=query) | Q(other_name__icontains=query))[:1]
            
                return render(request, 'user/register_name.html', {'persons': persons})
            else:
                messages.warning(request, "Empty search query, or your are not online learner")

                return redirect( 'mode')

        else:
            return render(request, 'user/register_name.html')



def verify_online(request, pk):
    online_learner= get_object_or_404(OnlineLearner, id=pk)
    person= Person.objects.get(id = online_learner.person.id)
    return render(request, 'user/online_detail.html' ,
                  {'online_learner':online_learner,
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

