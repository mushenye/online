from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from user.forms import  RegistrationForm


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
    
    
        
    return render(request, "user/userprofile.html")
    
# def userprofile(request):
#     current_user = request.user
#     email = current_user.email
#     if current_user.is_authenticated:
#         if email:
#             # Create a Contact object if it does not exist or get the object
#             contact, created = Contact.objects.get_or_create(user=current_user, email=email)
#             if created:
#                 messages.info(request, f'Welcome {current_user}, You are free to use our website')
#                 mycontact = get_object_or_404(Contact, user=current_user)
#                 form = ContactForm(instance=mycontact)
#                 if request.method == 'POST':
#                     form = ContactForm(request.POST, instance=mycontact)
#                     if form.is_valid():
#                         form.save()
#                         email=form.cleaned_data.get('email')
#                         messages.success(request,f"Your Email: {email} !!  ")
#                         return redirect('viewproduct')    
        
#                 return render(request, 'mybiz/contact.html', {'form': form})
#             else:
               
#                 return redirect('viewproduct')
#         else:
#             return redirect('register')
#     else:
#         return redirect('login')


# def send_message(request,pk):
#     user= request.user
#     product=ProductImage.objects.get(id=pk)
#     conversation, created = Conversation.objects.get_or_create( member=user, product=product)
#     if Conversation:
#         chat=Chat.objects.filter(product=product)


# def message_list(request):
#     messages = Chat.objects.filter(Q(sender=request.user)).order_by('-created_at')
#     return render(request, 'user/message_list.html', {'messages': messages})



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

