from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def register(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "The username is already taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "The email is already used")
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # Login after registering
                    # auth.login(request, user)
                    # messages.success(request, "Registered successfully")
                    # return redirect('index')
                    user.save()                   
                    messages.success(request, "Registered successfully")
                    return redirect('login')


        else:
            messages.error(request, 'Password not matched')
            return redirect('register')

    return render(request, 'accounts/register.html')


def login(request):
    if request.method == "POST":
        # login User
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username = username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,"Login successful")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    
    context = {
        'contacts':user_contacts
    }
    return render(request, 'accounts/dashboard.html',context)
