from django.db import models
from .utils import Flasher
import bcrypt
import re

class UserManager(models.Manager):
    def add(me,d):
        print(d)
        nid=0
        user_type=1
        if len(me.all())==0:
            user_type=9
        try:
            obj=me.create(
            first_name=d['user_fname'],
            last_name=d['user_lname'],
            email=d['user_email'],
            password=bcrypt.hashpw(d['user_password'].encode(), bcrypt.gensalt()).decode(),
            auth_level=user_type)
            print(f"Successfully added {d['user_fname']}!")
            nid=obj.id
        except Exception as er:
            print("Failure adding user.")
            print(type(er))
            print(er.args)
        return nid
    @staticmethod
    def hash_password(d):
        return bcrypt.hashpw(d['user_password1'].encode(), bcrypt.gensalt()).decode()
    def valid_name(me,error_loc,d):
        errors=[]
        # First Name
        V=d['user_fname']
        if not len(V)>=2:
             errors.append(f"{error_loc}|First Name must be 2 characters or more.")
        else:
            if not V.isalpha():
                 errors.append(f"{error_loc}|First Name must be letters only.")
        
        # Last Name
        V=d['user_lname']     
        if not len(V)>=2:
             errors.append(f"{error_loc}|Last Name must be 2 characters or more.")
        else:
            if not V.isalpha():
                 errors.append(f"{error_loc}|Last Name must be letters only.")
        return errors
    def valid_email(me,error_loc,d,prev_email):
        errors=[]
        V=d['user_email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not len(V)>=1:
            errors.append(f"{error_loc}|Email must not be empty.")
        else:
            if not EMAIL_REGEX.match(V):
                errors.append(f"{error_loc}|Email is not valid.")
            else:
                if not V == prev_email:
                    if len(me.filter(email=V))>0:
                        errors.append(f"{error_loc}|Email is already taken.")
        return errors
    def valid_password(me,error_loc,d):
        errors=[]
        V=d['user_password1']
        V2=d['user_password2']
        pw=True
        pw2=True
        
        if not len(V)>=8:
            errors.append(f"{error_loc}|Password must be 8 characters or more.")
            pw=False
        if not len(V2)>=8:
            errors.append(f"{error_loc}|Confirm Password must be 8 characters or more.")
            pw2=False
        
        if pw and pw2:
            if V != V2:
                errors.append(f"{error_loc}|Passwords do not match.")
        
        return errors
    def valid_reg(me,r,d,addme):
        e={}
        p=[]
        V=None
        T=''
        account=0
        try:
            
            # First Name
            V=d['user_fname']
            T='fname'
            
            if not len(V)>=2:
                e[T]="reg|First Name must be 2 characters or more."
            else:
                if not V.isalpha():
                    e[T]="reg|First Name must be letters only."
            
            # Last Name
            V=d['user_lname']
            T='lname'
            
            if not len(V)>=2:
                e[T]="reg|Last Name must be 2 characters or more."
            else:
                if not V.isalpha():
                    e[T]="reg|Last Name must be letters only."
            
            # Email
            V=d['user_email']
            T='email'
            
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not len(V)>=1:
                e[T]="reg|Email must not be empty."
            else:
                if not EMAIL_REGEX.match(V):
                    e[T]="reg|Email is not valid."
                else:
                    if len(me.filter(email=V))>0:
                        e[T]="reg|Email is already taken."
            # Password (Reg)
            V=d['user_password']
            V2=d['user_password2']
            T='password'
            T2='password2'
            pw=True
            pw2=True
            
            if not len(V)>=8:
                e[T]="reg|Password must be 8 characters or more."
                pw=False
            if not len(V2)>=8:
                e[T2]="reg|Confirm Password must be 8 characters or more."
                pw2=False
            
            if pw and pw2:
                if V != V2:
                    e[T]="reg|Passwords do not match."
            
            Flasher.push_messages(r,e,Flasher.error)
            if len(e)>0:
                p.append(f"reg_prev_fname|{d['user_fname']}")
                p.append(f"reg_prev_lname|{d['user_lname']}")
                p.append(f"reg_prev_email|{d['user_email']}")
                Flasher.push_messages(r,p,Flasher.info)
            else:
                print("Success!")
                if addme:
                    account=me.add(d)
        except KeyError as er:
            e['error']=f"reg|Request contained missing data. ({er.args[0]})"
            Flasher.push_messages(r,e,Flasher.error)
        except Exception as er:
            print(f"{type(er)}\nThere was a problem parsing data.")
            print(er.args)
        return {'error': len(e), 'id': account}
        
    def valid_login(me,r,d):
        e={}
        p=[]
        V=None
        T=''
        account=0
        try:
            
            # Email
            V=d['user_email']
            T='email'
            usr=True
            
            if not len(V)>=1:
                usr=False
                e[T]="login|Email must not be empty."
            else:
                cnt=len(me.filter(email=V))
                if cnt==0:
                    usr=False
                    e[T]="login|Email is not found."
                if cnt>1:
                    usr=False
                    e[T]="login|Emails of the same name found. Woah!"
                if cnt==1:
                    account=me.get(email=V).id

            # Password (Login)
            V=d['user_password']
            T='password'
            pw=True
            
            if not len(V)>=1:
                e[T]="login|Password must not be empty."
                pw=False
            
            if usr and pw:
                if not bcrypt.checkpw(V.encode(), me.get(id=account).password.encode()):
                     e[T]="login|Password is not correct."
                
            Flasher.push_messages(r,e,Flasher.error)
            if len(e)>0:
                p.append(f"login_prev_email|{d['user_email']}")
                Flasher.push_messages(r,p,Flasher.info)
                account=0
            else:
                print("Success!")
        except KeyError as er:
            e['error']=f"login|Request contained missing data. ({er.args[0]})"
            Flasher.push_messages(r,e,Flasher.error)
            account=0
        except Exception as er:
            print(f"{type(er)}\nThere was a problem parsing data.")
            print(er.args)
            account=0
        return {'error': len(e), 'id': account}
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    auth_level = models.IntegerField(default=1)
    desc = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"