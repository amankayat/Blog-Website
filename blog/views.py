
from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from blog.forms import signupform,loginform,addpostform
from .models import post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
# Create your views here.

def user_signup(requests):
    if not requests.user.is_authenticated:
        if requests.method=='POST':
            fm = signupform(requests.POST)
            if fm.is_valid():
                fm.save()
                messages.success(requests,"Congo! yu have registered successfully!!")
                return HttpResponseRedirect('/login/')
        else:
            fm = signupform()
        return render(requests,'blog/signup.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')

def user_login(requests):
    if not requests.user.is_authenticated:
        if requests.method== 'POST':
            fm = loginform(request=requests,data = requests.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user  = authenticate(username = uname,password = upass)
                if user is not None:
                    login(requests,user)
                    messages.success(requests,"Logged in successfully!!")
                    return HttpResponseRedirect('/profile/')
        else:
             fm = loginform()
        return render(requests,'blog/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')
   

def user_profile(requests):
    if requests.user.is_authenticated:
        posts = post.objects.all()
        user = requests.user
        name = user.get_full_name()
        return render(requests,'blog/profile.html',{'post':posts,'full_name':name,'user':user})
    else:
        return HttpResponseRedirect('/') 


def user_logout(requests):
    logout(requests)
    return HttpResponseRedirect('/')


def addpost(requests):
    if requests.user.is_authenticated:
        if requests.method=='POST':
            fm = addpostform(requests.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                subtitle = fm.cleaned_data['subtitle']
                desc = fm.cleaned_data['desc']
                pst = post(title=title,subtitle=subtitle,desc=desc)
                pst.save()
                messages.success(requests,"Posts added successfully!")
                return HttpResponseRedirect('/addpost/')
        else:
            fm = addpostform()
        return render(requests,'blog/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

def updateblog(requests,id):
    if requests.user.is_authenticated:
        pst = post.objects.get(pk=id)
        if requests.method =="POST":
            fm = addpostform(requests.POST,instance =pst)
            if fm.is_valid():
                fm.save()
                messages.success(requests,"Blog Updated Successfully!")
                return HttpResponseRedirect('/profile/')
        else:
            fm = addpostform(instance=pst)
        return render(requests,'blog/updatepost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

    
def deletepst(requests,id):
    pst = post.objects.filter(pk=id)
    pst.delete()
    messages.success(requests,"POST Deleted Successfully")
    return HttpResponseRedirect('/profile/')

def home(requests):
    posts = post.objects.all()
    return render(requests,'blog/home.html',{'posts':posts})

def about(requests):
    return render(requests,'blog/about.html')

def contact(requests):
    return render(requests,'blog/contact.html')

def showblog(requests,id):
    pi = post.objects.get(pk=id)
    return render(requests,'blog/showblog.html',{'user':pi})