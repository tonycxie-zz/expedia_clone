from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime

class UsersManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "First name is required"
        elif not NAME_REGEX.match(postData["first_name"]):
            errors["first_name"] = "First name must be at least 2 letters and have no numbers"
        if len(postData["last_name"]) < 1:
            errors["last_name"] = "Last name is required"
        elif not NAME_REGEX.match(postData["last_name"]):
            errors["last_name"] = "Last name must be at least 2 letters and have no numbers"
        if len(postData["reg_email"]) < 1:
            errors["reg_email"] = "Email is required"
        elif not EMAIL_REGEX.match(postData["reg_email"]):
            errors["reg_email"] = "Invalid email"
        elif Users.objects.filter(email = postData["reg_email"]).count() > 0:
            errors["reg_email"] = "Email already exists"
        if len(postData["password"]) < 1:
            errors["pw"] = "Password is required"
        elif len(postData["password"]) < 9:
            errors["pw"] = "Password must be at least 8 characters"
        if len(postData["confirm_password"]) < 1:
            errors["confirm_pw"] = "You must confirm your password"
        elif postData["password"] != postData["confirm_password"]:
            errors["confirm_pw"] = "Password does not match"
        return errors

class TripsManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData["destination"]) < 1:
            errors["destination"] = "Destination is required"
        if len(postData["desc"]) < 1:
            errors["desc"] = "Description is required"
        if len(postData["start_date"]) < 1:
            errors["start_date"] = "Start date is required"
        elif datetime.strptime(postData["start_date"], "%Y-%m-%d") <= datetime.now():
            errors["start_date"] = "Start date must be in the future"
        if len(postData["end_date"]) < 1:
            errors["end_date"] = "End date is required"
        elif datetime.strptime(postData["end_date"], "%Y-%m-%d") <= datetime.now():
            errors["end_date"] = "End date must be in the future"
        elif datetime.strptime(postData["end_date"], "%Y-%m-%d") < datetime.strptime(postData["start_date"], "%Y-%m-%d"):
            errors["end_date"] = "End date cannot be before start date"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password_hash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    planner = models.ForeignKey(Users, related_name = "planned_trip")
    joiners = models.ManyToManyField(Users, related_name = "joined_trip")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripsManager()