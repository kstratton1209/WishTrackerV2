from django.shortcuts import render, HttpResponse, redirect
from .models import Registration, RegistrationManager
from django.contrib import messages
import bcrypt

def index(request):

    return render(request,"index.html")

def register(request):
    
    errors = Registration.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        first_name_from_form = request.POST['first_name']
        last_name_from_form = request.POST['last_name']
        email_from_form = request.POST['email']
        password_from_form = request.POST['password']

        pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt()).decode()
        Registration.objects.create(first_name=first_name_from_form, last_name= last_name_from_form, email = email_from_form, password=pw_hash)

        request.session['email']=email_from_form
        user = Registration.objects.filter(email = email_from_form)
        if user:
            logged_user = user[0]
            request.session['first_name']=logged_user.first_name
            request.session['email']=logged_user.email
            request.session['id']=logged_user.id

        return redirect('/success')

def login(request):
    user = Registration.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['first_name']=logged_user.first_name
            request.session['id']=logged_user.id

            return redirect('/success')
    else:
        errors = {}
        if len(request.POST['password']) == 0:
            errors["password"] = "Please enter a password."
        if len(request.POST['email']) == 0:
            errors["email"] = "Please enter an email."
        else:
            errors["confirm"] = "Password or email is incorrect. Please try again."
        
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect("/")

def success(request):
    return redirect("content/home")

def logout(request):

    del request.session['first_name']
    del request.session['id']
    return redirect("/")