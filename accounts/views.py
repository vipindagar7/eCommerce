from django.shortcuts import render , HttpResponse , redirect
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout

from .models import *
import uuid
from .email import *

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        auth = authenticate(request , email=email, password=password)
        if auth:
            login(request, auth)
            if request.user.is_seller:
                return redirect('/shop/manage_products/')
            elif request.user.is_superuser:
                return redirect('/accounts/manage_users/')
            else:                
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/accounts/login/')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_seller = request.POST.get('is_seller')
        if is_seller == "on":
            is_seller = True
        else:
            is_seller = False
        try:
                if CustomUser.objects.filter(email=email).first():
                    messages.error(request,  email + " is already taken")
                    return redirect('/accounts/signup/')
                auth_token =  str(uuid.uuid4())
                user_obj = CustomUser.objects.create_user(email=email , first_name=first_name, last_name=last_name , auth_token =auth_token, is_seller = is_seller)
                user_obj.set_password(password)
                user_obj.save()
                # send_verification_email(email , auth_token)
                # if send_verification_email:                
                messages.success(request, "check" + email + " for verification link")
                return redirect('/accounts/login/')    
        except Exception as e:
            return HttpResponse(e)
    context = {}
    return render(request, "accounts/signup.html" , context)
        
def verify_mail(request , auth_token):
    try:
        user = CustomUser.objects.filter(auth_token=auth_token).first()
        if user:
            if user.is_verified:
                messages.success(request, "user is already verified")
                return redirect("/accounts/login/")
            user.is_verified = True
            user.save()
            messages.success(request, "user has been verified")
            return redirect("/accounts/login/")
        else:
            messages.error(request, "user not found")
            return redirect("/accounts/login/")
    except Exception as e:
        return HttpResponse(e)
    
    
    
    
    
def profile(request):
    user = request.user
    
    if user.is_seller:
        
        profile = SellerProfile.objects.get(user = user)
    else:
        profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')
        if request.user.is_seller:
            profile.alt_phone = request.POST.get('alt_phone')
            profile.shop_name = request.POST.get('shop_name')
            profile.gst_number = request.POST.get('gst_number')
            profile.pan_number = request.POST.get('pan_number')
            
        profile.save()
        messages.success(request, "profile updated successfully")
        return redirect("/accounts/profile")
    addr = address.objects.filter(user = request.user)
    context = {'profile':profile , 'addr':addr}
    return render(request , 'accounts/profile.html' , context)
    

    
def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        new_password_confirmation = request.POST.get('new_password_confirmation')
        if new_password == new_password_confirmation:
            user = CustomUser.objects.get(email= request.user)                
            user.set_password(new_password_confirmation)
            user.save()
            messages.success(request, "Password changed")
            return redirect('/')
        else:
            messages.error(request, "Password not matched")
            return redirect('/accounts/profile/')    
      
def change_email(request):
    if request.method == "POST":
        new_email = request.POST.get('new_email')
        if CustomUser.objects.filter(email = new_email).first():
            messages.error(request, "email already taken")
            return redirect('/accounts/profile/')
        else:
            send_verification_new_email(new_email, request.user.auth_token)
            user = CustomUser.objects.get(email= request.user.email)                
            user.is_verified = False
            user.email = new_email
            user.save()
            messages.success(request, f"check {new_email} for verification link")
            return redirect('/accounts/profile/')
    return HttpResponse("404 page not found")



def delete_user(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = authenticate(request , email = request.user.email , password = password)
        if user is not None:
            user = CustomUser.objects.get(email= request.user.email)                
            user.delete()
            send_delete_account_mail(request.user.email)
            messages.success(request, "user deleted")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/accounts/settings/')
    return HttpResponse("404 page not found")

def add_address(request):
    if request.method == 'POST':
        addr = address(user=request.user, address=request.POST.get('address'))
        addr.save()
        messages.success(request , 'address added successfully')
        return redirect('/accounts/profile/')
        
    return render(request , 'accounts/add_address.html')

def edit_address(request , id):
    addr = address.objects.get(id = id)
    if request.method == 'POST':
        addr.address = request.POST.get('address')
        addr.save()
        return redirect('/accounts/profile/')
    context = {'addr': addr}
    messages.success(request , 'address updated successfully')
    return render(request , 'accounts/edit_address.html' , context)

def delete_address(request , id):
    addr = address.objects.get(id = id)
    addr.delete()
    messages.error(request,  "address deleted")
    return redirect('/accounts/profile/')



class AdminActions:
    
    def manage_users(request):
        if request.user.is_superuser:
            users = CustomUser.objects.filter(is_superuser=False)
            context = {'users': users}
            return render(request, 'accounts/admin/manage_users.html', context)
        else:
            return HttpResponse('your are not allowed to manage users')
    
    def view_user(request, id):
        if request.user.is_superuser:
            user = CustomUser.objects.filter(id=id).first()
            context = {'user': user}
            return render(request, 'accounts/admin/view_user.html', context)
        else:
            return HttpResponse('your are not allowed to manage users')

    def delete_user_by_admin(request, id):
        if request.user.is_superuser:
            user = CustomUser.objects.get(id=id)
            user.delete()
            messages.success(request,"user deleted successfully")
            return redirect('/accounts/manage_users/')