from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .forms import LoginForm , UpdateUserForm
from django.contrib.auth.models import User  #djnago built-in User Model

from payment.forms import ShippingForm  # import payments forms here
from payment.models import ShippingAddress  # import payments models here

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth  #login view
from django.contrib.auth import authenticate, login, logout #login view
from django.contrib.auth.decorators import login_required

from django.contrib import messages  #django messages


# Normal registraion Start 
"""
def register(request):

    form = CreateUserForm()

    if request.method == 'POST': 
        form = CreateUserForm(request.POST)  #hold here submited data
        if form.is_valid():
            form.save()
            return redirect('store')
    
    context = {'form':form}  #context bc we have to use this on html templates

    return render(request, 'account/registration/register.html', context=context)
"""
#Normal registraion End

#Tokenization Registration Start
def register(request):

    form = CreateUserForm()

    if request.method == 'POST': 
        form = CreateUserForm(request.POST)  #hold here submited data
        if form.is_valid():
            user = form.save()  #user object create but by-default user True thakbe
            user.is_active = False  #user ke active na kora without click on link
            user.save()              #save user in db
 
            #Email Verification Setup (Templates)
            current_site = get_current_site(request)
            subject = 'Account Verification Email!'
            message = render_to_string('account/registration/email-verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message) #send email user register mail that give on register form

            return redirect('email-verification-sent') 

    
    context = {'form':form}  #context bc we have to use this on html templates

    return render(request, 'account/registration/register.html', context=context)

#Tokenization Registration End


#register email verification flow Start

def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    #success
    if user and user_tokenizer_generate.check_token(user,token):

        user.is_active = True
        user.save()
        return redirect('email-verification-success') 

    #failed
    else:
        return redirect('email-verification-failed') 



def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


#register email verification flow End


# Login flow START

def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request,user)

                return redirect('dashboard')
    context = {'form': form}

    return render(request , 'account/my-login.html', context=context)


# Login flow END


# Logout flow Start
def user_logout(request):
    try:

        for key in list(request.session.keys()):

            if key == 'cart':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    #auth.logout(request)
    messages.success(request, "Logout Succesfull!")
    return redirect('store')


# dashboard
@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):

    user_form = UpdateUserForm(instance=request.user)  #its here bc update validation error shows
    # Updating Our Username and Email Here
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)  #grap current single user
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Your account updated successfully!")
            return redirect('dashboard')
        
    

    context = {'user_form': user_form}
    return render(request, 'account/profile-management.html', context=context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id = request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, "Your account deleted!")
        return redirect('store')
    return render(request, 'account/delete-account.html')

#Shiping View START
#@login_required(login_url='my-login')
def manage_shipping(request):
    try:
        # account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        # account user with no shipment information
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():

            # Assign the user FK on the object
            shipping_user = form.save(commit=False)

            #adding the foreign key itself
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')
    
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context)
            

#Shiping View END