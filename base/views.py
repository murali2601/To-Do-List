from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
# Create your views here.

def home(request):
    user = User.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User doesnot exists")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('todo',  id=user.id  )
        else:
            messages.error(request,"User name or password is invalid")
        return redirect('home')
   
    return render(request,'base/login.html')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('todo' ,id=user.id)
        else:
            messages.error(request," An unexpected error occured !")
    return render(request,'base/register.html',{'form' : form})

def logoutUser(request):

    logout(request)
    return redirect('home')

@login_required(login_url='home')
def todo(request,id):
    user = User.objects.get(id=id)
    tasks = Task.objects.all().order_by('-created')
    if request.method == 'POST':
        data = request.POST
        tasks = Task.objects.create(
            author = request.user,
            todo = data['add'],
        )
        print('author : ',tasks.author.id)
        print('request : ',request.user.id)
        return redirect('todo', id=user.id)
    context = {
        'tasks' : tasks
    }
    return render(request, 'base/home.html',context)

def update(request,pk):
    update = Task.objects.get(id=pk)
    forms = TaskForm(instance=update)

    if request.method == 'POST':
        forms = TaskForm(request.POST, instance=update)
        if forms.is_valid():
            forms.save()
        return redirect('todo', id=update.author.id)
    context = {
        'update' : update,
        'forms' : forms
    }

    return render(request, 'base/update.html',context)


def delete(request,pk):
    delete = Task.objects.get(id=pk)
    if request.method == 'POST':
        delete.delete()
        return redirect('todo', id=delete.author.id)
    context = {
        'delete' : delete
    }

    return render(request, 'base/delete.html',context)