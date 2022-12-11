from django.shortcuts import render
from .models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import json
from . import urls
# Create your views here.


def register(request):
    if request.method == "POST":
        user = User()
        user.name = request.POST.get("name")
        user.age = int(request.POST.get("age"))
        if user.age < 18 or user.age > 65:
            return render(request, "user/register.html", {
                "message": "Age should be between 18-65"
            })
        user.email = request.POST.get("email")
        if User.objects.filter(email=user.email).exists():
            return render(request, "user/register.html", {
                "message": "User already exists"
            })
        request.session['username'] = user.email
        user.save()
        return HttpResponseRedirect(reverse('all'))
    return render(request, "user/register.html")


def all_classes(request):
    if request.session.has_key('username'):
        email = request.session['username']
        user = User.objects.get(email=email)
        months = user.months.split(',')
        while ('' in months):
            months.remove('')
        print(months)
        return render(request, "user/all.html", {
            "months": months
        })
    else:
        return HttpResponseRedirect(reverse("register"))


def book(request):
    if request.session.has_key('username'):
        email = request.session['username']
        user = User.objects.get(email=email)
        if request.method == "GET":
            months = []
            if user.months is None:
                months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'Novemeber', 'December']
            else:
                allmonths = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'Novemeber', 'December']
                months = user.months.split(',')
                print(months, user.months)
                allmonths, months = list(set(allmonths).difference(
                    months)), list(set(allmonths).difference(months))
                print(months, allmonths)
                months = allmonths

            return render(request, "user/book.html", {
                "months": months
            })
        if request.method == "POST":
            month = request.POST.get("month")
            print(month)
            if user.months is not None:
                user.months += ','+month
            else:
                user.months = month
            user.save()
            return HttpResponseRedirect(reverse("book"), {
                "message": "Booked Successfully"
            })
    return HttpResponse("<h1>Please Login or regsiter</h1>")


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        print(user)
        if user is None:
            return HttpResponseRedirect(reverse('register'), {
                "meesage": "Register First"
            })
        else:
            request.session['username'] = user.email
            months = user.months.split(',')
            while ('' in months):
                months.remove('')
            print(months)
            return HttpResponseRedirect(reverse("all"))
    return render(request, 'user/login.html')


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'user/register.html', {
        "message": "Loggedout Succesfully"
    })
