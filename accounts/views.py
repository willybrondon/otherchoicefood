from django.shortcuts import render, redirect
from .forms import  UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

# restrict the vendor to accessing the customer page for

# restrict the customer to accessing the vendor page 
def  check_role_vendor(user):
    if user.role == 1:
        return True
    else:
     raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True 
    else :
        raise PermissionDenied  
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')

    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'you are now logged in. ')
                return redirect('myAccount')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
    return render(request, 'accounts/login.html')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have logged out. ')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)

    return redirect(redirectUrl)
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')