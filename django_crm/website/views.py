from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

""" Лог и логаут - редирект на домашний юрл.
    асист через меседж=хэлпер
    
    если записи нет:
                регаемся
    если запись есть:
                редирект=хоум
"""


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You've been logged in")
            return redirect('home')
        else:
            messages.warning(request, "A mistake occurred, try one more time")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You logged out")
    return redirect('home')


def register_user(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've been register in")
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration!")

    return render(request, 'register.html', {'form': form})


def record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, "record.html", {"record": record})
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        del_record = Record.objects.get(id=pk)
        del_record.delete()
        messages.success(request, "You deleted the record")
        return redirect("home")
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if form.is_valid():
            add_record = form.save()
            messages.success(request, f"Record {add_record.first_name} was added")
            return redirect("home")
        return render(request, "add_record.html", {"form": form})
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            updated_record = form.save()
            messages.success(request, f"Record '{updated_record.first_name}' was added")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.error(request, "You have to login")
        return redirect("home")
