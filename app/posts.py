from django.shortcuts import render, HttpResponse, redirect 
from django.http import JsonResponse 
from login.models import *
from .models import *
from login.utils import MessageSplit,Flasher

def admins_add(request):
    admin_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            admin_user=User.objects.get(id=request.session['user']['id'], auth_level=9)
            print("Admin:",admin_user.id)
            errors=[]
            type_of="aa"
            
            errors.extend(User.objects.valid_name(type_of,request.POST))
            errors.extend(User.objects.valid_email(type_of,request.POST,""))
            errors.extend(User.objects.valid_password(type_of,request.POST))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user=User()
                my_user.first_name=request.POST['user_fname']
                my_user.last_name=request.POST['user_lname']
                my_user.email=request.POST['user_email']
                my_user.password=User.objects.hash_password(request.POST)
                my_user.save()
                if not request.GET.get('q', '')=="debug":
                    return redirect("/dashboard/admin")
        except User.DoesNotExist:
            Flasher.push_messages(request,"aa|Access denied.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/users/new")
    
def admins_edit_info(request):
    admin_user=None
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            admin_user=User.objects.get(id=request.session['user']['id'], auth_level=9)
            my_user=User.objects.get(id=request.POST['user_id'])
            print("Admin:",admin_user.id)
            print("Target:",my_user.id)
            errors=[]
            type_of="aei"
            
            errors.extend(User.objects.valid_name(type_of,request.POST))
            errors.extend(User.objects.valid_email(type_of,request.POST,my_user.email))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user.auth_level=1
                if request.POST['user_level']=="admin":
                    my_user.auth_level=9
                my_user.email=request.POST['user_email']
                my_user.first_name=request.POST['user_fname']
                my_user.last_name=request.POST['user_lname']
                my_user.save()
            if not request.GET.get('q', '')=="debug":
                 return redirect(f"/users/edit/{my_user.id}")
        except User.DoesNotExist:
            Flasher.push_messages(request,"aei|Access denied, or the user not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard")
    
def admins_edit_password(request):
    admin_user=None
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            admin_user=User.objects.get(id=request.session['user']['id'], auth_level=9)
            my_user=User.objects.get(id=request.POST['user_id'])
            print("Admin:",admin_user.id)
            print("Target:",my_user.id)
            errors=[]
            type_of="aep"
            
            errors.extend(User.objects.valid_password(type_of,request.POST))

            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user.password=User.objects.hash_password(request.POST)
                my_user.save()
            if not request.GET.get('q', '')=="debug":
                 return redirect(f"/users/edit/{my_user.id}")
        except User.DoesNotExist:
            Flasher.push_messages(request,"aep|Access denied, or the user is not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard")



def users_edit_info(request):
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            my_user=User.objects.get(id=request.session['user']['id'])
            print(my_user.id)
            errors=[]
            type_of="uei"
            
            errors.extend(User.objects.valid_name(type_of,request.POST))
            errors.extend(User.objects.valid_email(type_of,request.POST,my_user.email))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user.email=request.POST['user_email']
                my_user.first_name=request.POST['user_fname']
                my_user.last_name=request.POST['user_lname']
                my_user.save()
        except User.DoesNotExist:
            Flasher.push_messages(request,"uei|User not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/users/edit")
    
def users_edit_password(request):
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            my_user=User.objects.get(id=request.session['user']['id'])
            print(my_user.id)
            errors=[]
            type_of="uep"
            
            errors.extend(User.objects.valid_password(type_of,request.POST))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user.password=User.objects.hash_password(request.POST)
                my_user.save()
        except User.DoesNotExist:
            Flasher.push_messages(request,"uep|User not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/users/edit")
    
def users_edit_desc(request):
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            my_user=User.objects.get(id=request.session['user']['id'])
            print(my_user.id)
            errors=[]
            type_of="ued"
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                my_user.desc=request.POST['user_desc']
                my_user.save()
        except User.DoesNotExist:
            Flasher.push_messages(request,"ued|User not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/users/edit")
    



def msgs_profile(request):
    my_poster=None
    my_user=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            my_poster=User.objects.get(id=request.session['user']['id'])
            my_user=User.objects.get(id=request.POST['msg_userid'])
            print(my_user.id)
            errors=[]
            type_of="mp"
            
            errors.extend(Comment.objects.valid(type_of,request.POST))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                Comment.objects.create(text=request.POST['msg_text'],poster=my_poster,user=my_user)
            if not request.GET.get('q', '')=="debug":
                 return redirect(f"/users/show/{my_user.id}")
        except User.DoesNotExist:
            Flasher.push_messages(request,"mp|User(s) not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard")
    
def msgs_message(request):
    my_poster=None
    my_comment=None
    if request.method=="POST" and 'user' in request.session:
        print(request.POST)
        try:
            my_poster=User.objects.get(id=request.session['user']['id'])
            my_comment=Comment.objects.get(id=request.POST['msg_id'])
            print(my_poster.id)
            errors=[]
            type_of="mm"
            
            errors.extend(SubComment.objects.valid(type_of,request.POST))
            
            if len(errors)>0:
               Flasher.push_messages(request,errors,Flasher.error)   
               prev_data=[]
               for k,v in request.POST.items():
                   prev_data.append(f"prev_{type_of}_{k}|{v}")
               Flasher.push_messages(request,prev_data,Flasher.info)
            else:
                thing=SubComment.objects.create(text=request.POST['msg_text'],poster=my_poster,parent_comment=my_comment)
            if not request.GET.get('q', '')=="debug":
                return redirect(f"/users/show/{my_comment.user.id}")
        except Comment.DoesNotExist:
            Flasher.push_messages(request,"mm|Comment not found.",Flasher.error)
        except User.DoesNotExist:
            Flasher.push_messages(request,"mm|User not found.",Flasher.error)
        except Exception as er:
            print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard")
    
def delete_user(request, id):
    admin_user=None
    my_user=None
    try:
        admin_user=User.objects.get(id=request.session['user']['id'], auth_level=9)
        my_user=User.objects.get(id=id)
        print("Admin:",admin_user.id)
        print("Target:",my_user.id)
        if not admin_user.id == my_user.id:
            my_user.delete()
        else:
            print("Denied. You cannot delete yourself.")
    except Exception as er:
        print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard/admin")
    
def delete_comment(request, id):
    my_user=None
    my_comment=None
    try:
        my_user=User.objects.get(id=request.session['user']['id'])
        my_comment=Comment.objects.get(id=id)
        my_page=my_comment.user.id
        if my_comment.poster.id == my_user.id:
            my_comment.delete()
        else:
            print("Denied. You cannot another user's comment.")
        if not request.GET.get('q', '')=="debug":
            return redirect(f"/users/show/{my_page}")
    except Exception as er:
        print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard/admin")
    
def delete_subcomment(request, id):
    my_user=None
    my_comment=None
    try:
        my_user=User.objects.get(id=request.session['user']['id'])
        my_comment=SubComment.objects.get(id=id)
        my_page=my_comment.parent_comment.user.id
        if my_comment.poster.id == my_user.id:
            my_comment.delete()
        else:
            print("Denied. You cannot another user's sub-comment.")
        if not request.GET.get('q', '')=="debug":
            return redirect(f"/users/show/{my_page}")
    except Exception as er:
        print(type(er),er)
    if request.GET.get('q', '')=="debug":
        return redirect("/debug")
    return redirect("/dashboard/admin")