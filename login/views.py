from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .utils import MessageSplit

def index(request):
    if 'user' in request.session:
        return redirect("/")
    context={
        'msg': MessageSplit.parse(request)
    }
    return render(request,"login.html",context)

def test(request): 
    test={}
    """
    test['user_fname']="Fred"
    test['user_lname']="Fuchs"
    test['user_email']="shittygamethatsucksass@gmail.com"
    test['user_password']="firfer"
    test['user_password2']="firfer"
    errors=User.objects.valid_reg(request, test, True)
    """
    test['user_email']="toropiamon@gmail.com"
    test['user_password']="firfer"
    errors=User.objects.valid_login(request, test)
    print(errors)
    print(MessageSplit.parse(request))
    print(User.objects.get(id=errors['id']).__dict__)
    return HttpResponse("Login Page") 

def user_reg(request):
    if 'user' in request.session:
        return redirect("/")
    if request.method=="POST":
        print(request.POST)
        user=User.objects.valid_reg(request, request.POST, True)
        if user['error']:
            return redirect("/auth")
        request.session['user']={}
        request.session['user']['id']=user['id']
    return redirect("/")

def user_login(request):
    if 'user' in request.session:
        return redirect("/")
    if request.method=="POST":
        print(request.POST)
        user=User.objects.valid_login(request, request.POST)
        if user['error']:
            return redirect("/auth")
        request.session['user']={}
        request.session['user']['id']=user['id']
    return redirect("/")

def user_logout(request):
    try:
        del request.session['user']
    except:
        pass
    return redirect("/")