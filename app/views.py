from django.shortcuts import render, HttpResponse, redirect 
from django.http import JsonResponse 
from login.models import *
from .models import *
from login.utils import MessageSplit,Flasher

def index(request):
    context = {
        'me': None,
        'pg': "home"
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
    return render(request,"index.html",context)

def pg_signin(request):
    context = {
        'me': None,
        'pg': "signin",
        'pg_type': 1,
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        return redirect("/dashboard")
    return render(request,"signin_reg.html",context)

def pg_register(request):
    context = {
        'me': None,
        'pg': "reg",
        'pg_type': 2,
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        return redirect("/dashboard")
    return render(request,"signin_reg.html",context)

def pg_add(request):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'pg': "reg",
        'pg_type': 3,
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        if not context['me'].auth_level==9:
            return redirect("/")
    return render(request,"signin_reg.html",context)

def pg_dashboard(request):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'pg': "dashboard",
        'pg_title': "All Users",
        'admin': 0,
        'users': User.objects.all(),
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        if context['me'].auth_level==9:
            return redirect("/dashboard/admin")
    return render(request,"dashboard.html",context)

def pg_dashboard_admin(request):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'pg': "dashboard",
        'pg_title': "Manage Users",
        'admin': 1,
        'users': User.objects.all(),
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        if not context['me'].auth_level==9:
            return redirect("/dashboard")
    return render(request,"dashboard.html",context)

def pg_profile(request):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'pg': "profile",
        'pg_title': "Edit Profile",
        'layout': 0,
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
    return render(request,"profile.html",context)

def pg_edit_user(request, id):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'user': None,
        'pg': "edit_user",
        'pg_title': f"Edit User #{id}",
        'layout': 1,
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
        if not context['me'].auth_level==9:
            return redirect("/")
    try:
        context['user']=User.objects.get(id=id)
        context['pg_title']+=f": {context['user'].first_name} {context['user'].last_name}"
    except:
        return redirect("/dashboard/admin")
    return render(request,"profile.html",context)

def pg_show_user(request, id):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': None,
        'user': None,
        'pg': "show_user",
        'comments': [],
        'msg': MessageSplit.parse(request)
    }
    if 'user' in request.session:
        context['me']=User.objects.get(id=request.session['user']['id'])
    try:
        context['user']=User.objects.get(id=id)
        context['comments']=Comment.objects.filter(user__id=id)
        print(context['comments'])
    except Exception as er:
        print(type(er),er)
        return redirect("/dashboard")
    return render(request,"user.html",context)

def user_reg(request):
    if 'user' in request.session:
        return redirect("/")
    if request.method=="POST":
        print(request.POST)
        user=User.objects.valid_reg(request, request.POST, True)
        if user['error']:
            return redirect("/register")
        request.session['user']={}
        request.session['user']['id']=user['id']
    return redirect("/dashboard")

def user_login(request):
    if 'user' in request.session:
        return redirect("/")
    if request.method=="POST":
        print(request.POST)
        user=User.objects.valid_login(request, request.POST)
        if user['error']:
            return redirect("/signin")
        request.session['user']={}
        request.session['user']['id']=user['id']
    return redirect("/dashboard")

def user_logout(request):
    try:
        del request.session['user']
    except:
        pass
    return redirect("/")

def debug(request):
    if 'user' not in request.session:
        return redirect("/")
    context = {
        'me': User.objects.get(id=request.session['user']['id']),
        'users': User.objects.all(),
        'comments': Comment.objects.all(),
        'subcomments': SubComment.objects.all(),
        'msg': MessageSplit.parse(request)
    }
    for k,v in context['msg'].items():
        print(k,v)
    #print(Book.objects.authors())
    return render(request,"debug.html",context)
    
def what(request, exception):
    return HttpResponse("Oh! So you are the error?")