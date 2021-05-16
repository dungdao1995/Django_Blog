from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid(): #check the valid with the username
            form.save() #auto save form =>> can access to the admin page to control
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})

#IF we did not login, we need to login before access to profile 
@login_required #decorator: add function to the function
def profile(request):
    if request.method == "POST": #submit the data
        u_form = UserUpdateForm(request.POST,  #the method is the POST
                                instance = request.user) #instance means that: current infor will be automatically fulfilled in the update form
        p_form = ProfileUpdateForm(request.POST, #the method is the POST
                                    request.FILES, #the method is the File for updating the image
                                    instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid(): # press the update button to SUBMIT the new update
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!!') # feedback 
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

