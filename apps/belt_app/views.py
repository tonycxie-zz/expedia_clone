from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime


def index(request):
    return render(request, "belt_app/index.html")


def login(request):
    request.session["login_email"] = request.POST["login_email"]
    if Users.objects.filter(email = request.POST["login_email"]).count() > 0:
        user = Users.objects.get(email = request.POST["login_email"])
        if bcrypt.checkpw(request.POST["password"].encode(), user.password_hash.encode()):
            request.session["first_name"] = user.first_name
            request.session["last_name"] = user.last_name
            return redirect("/travels")
    messages.error(request, "You could not be logged in")
    return redirect("/")


def register(request):
    if request.method == "POST":
        request.session["first_name"] = request.POST["first_name"]
        request.session["last_name"] = request.POST["last_name"]
        request.session["reg_email"] = request.POST["reg_email"]
        errors = Users.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        Users.objects.create(
            first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"],
            email = request.POST["reg_email"],
            password_hash = pw_hash
        )
    return redirect("/travels") 

def travels(request):
    if request.session.get("login_email"):
        request.session["email"] = request.session["login_email"]
    else:
        request.session["email"] = request.session["reg_email"]
    user = Users.objects.get(email = request.session["email"])
    request.session["userid"] = user.id
    context = {
        "user": user,
        "your_trips": Trips.objects.filter(joiners = Users.objects.get(id = request.session["userid"])),
        "other_trips": Trips.objects.exclude(joiners = Users.objects.get(id = request.session["userid"])) 
    }
    return render(request, "belt_app/travels.html", context)


def logout(request):
    request.session.flush()
    return redirect("/")


def add_trip(request):
    return render(request, "belt_app/add.html")


def new_trip(request):
    if request.method == "POST":
        request.session["destination"] = request.POST["destination"]
        request.session["desc"] = request.POST["desc"]
        errors = Trips.objects.trip_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/addtrip")
        Trips.objects.create(
            destination = request.POST["destination"],
            desc = request.POST["desc"],
            start_date = request.POST["start_date"],
            end_date = request.POST["end_date"],
            planner_id = request.session["userid"]
        )
        trip = Trips.objects.get(destination = request.POST["destination"])
        trip.joiners.add(Users.objects.get(id = request.session["userid"]))
    return redirect("/travels")


def join(request, number):
    trip = Trips.objects.get(id = number)
    trip.joiners.add(Users.objects.get(id = request.session["userid"]))
    return redirect("/travels")


def cancel(request, number):
    trip = Trips.objects.get(id = number)
    trip.joiners.remove(Users.objects.get(id = request.session["userid"]))
    return redirect("/travels")


def delete(request, number):
    Trips.objects.get(id = number).delete()
    return redirect("/travels")


def view(request, number):
    trip = Trips.objects.get(id = number)
    context = {
        "trip": trip,
        "joiners": Users.objects.filter(joined_trip = trip).exclude(id = trip.planner_id)  
    }
    return render(request, "belt_app/view.html", context)