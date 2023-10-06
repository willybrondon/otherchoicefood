from django.shortcuts import render, redirect
from .forms import  UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # creat fomr using form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # create the user using create user method 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username, password=password,email=email)
            user.role = user.CUSTOMER
            user.save()
            messages.success(request,"your account has been register sucessfully")
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        
        form = UserForm()
    context = {
        'form':form,
        }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username, password=password,email=email)
            user.role = user.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been regsited sucessfully ! please wait for approval')
            return redirect('registerVendor')
        else:
            print('Invalid data')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {'form':form,
                'v_form': v_form,}
    
    return render(request, 'accounts/registerVendor.html', context)