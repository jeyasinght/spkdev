from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def dologin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dohome')
            # Redirect to a success page.
        else:
            messages.success(request, "There was an error, Try login again...!")
            return redirect('dologin')
            # Return an 'invalid login' error message
    else:
        return render(request, 'dologin.html')


def dohome(request):
    return render(request, 'dohome.html')


def dologout(request):
    logout(request)
    messages.success(request, "You were logged out ...!")
    return redirect('dologin')

