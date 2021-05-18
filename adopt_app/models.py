from django.db import models
from datetime import date, datetime
from time import strptime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, form):
        errors = {}
        if len(form["first_name"]) < 2:
            errors["first_name"] = "First Name is required and must be at least 2 characters!"
        if len(form["last_name"]) < 2:
            errors["last_name"] = "Last Name is required and must be at least 2 characters!"
        if len(form["user_affiliation"]) < 2:
            errors["user_affiliation"] = "Affiliation is required and must be at least 2 characters!"
        if not EMAIL_REGEX.match(form["user_email"]):          
            errors["user_email"] = ("Email required!")
        users_with_email = User.objects.filter(user_email = form["user_email"])
        if len(users_with_email) >= 1:
            errors["duplicate"] = "Email already exists."
        if len(form["user_address"]) < 2:
            errors["user_address"] = "Address is required and must be at least 2 characters!"
        if len(form["user_city"]) < 2:
            errors["user_city"] = "City is required and must be at least 2 characters!"
        if len(form["user_state"]) != 2:
            errors["user_state"] = "State is required and must be 2 characters!"
        if len(form["user_zipcode"]) != 5:
            errors["user_zipcode"] = "Zip Code is required and must be 5 characters!"
        if len(form["password"]) < 8:
            errors["password"] = "Password is required and at least 8 characters!"
        if form["password"] != form["confirm_pw"]:
            errors["pw_match"] = "Password must match!"
        return errors

    def login_validator(self, form):
        errors = {}
        check = User.objects.filter(user_email=form["user_email"])
        if not check:
            errors["user_email"] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(form["password"].encode(), check[0].password.encode()):
                errors["user_email"] = "Email and password do not match."
        return errors

class PetManager(models.Manager):
    def pet_validator(self, form):
        errors = {}

        if len(form['name']) < 3:
            errors['name'] = "A pet name must be provided and consist of at least 3 characters!"
        if len(form['animal']) < 2:
            errors['animal'] = "Animal type must be provided and consist of at least 2 characters!"
        if len(form['age']) < 1:
            errors['age'] = "A pet age must be provided and consist of at least 3 characters!"
        if len(form['sex']) < 1:
            errors['sex'] = "A pet sex must be provided and consist of at least 1 characters!"
        if len(form["pet_city"]) < 2:
            errors["pet_city"] = "City is required and must be at least 2 characters!"
        if len(form["pet_state"]) != 2:
            errors["pet_state"] = "State is required and must be 2 characters!"
        if len(form["pet_zip_code"]) != 5:
            errors["pet_zip_code"] = "Zip Code is required and must be 5 characters!"
        if len(form["pet_affiliation"]) < 2:
            errors["pet_affiliation"] = "Affiliation is required and must be at least 2 characters!"
        if len(form["description"]) < 3:
            errors["description"] = "A pet description must be provided and consist of at least 3 characters!"   
        if len(form["status"]) < 3:
            errors["status"] = "Pet status must be provided and consist of at least 3 characters!"  
        return errors

class AdoptManager(models.Manager):
    def adopt_validator(self, form):
        errors = {}

    
        if len(form["adopt_fname"]) < 2:
            errors["adopt_fname"] = "First Name is required and must be at least 2 characters!"
        if len(form["adopt_lname"]) < 2:
            errors["adopt_lname"] = "Last Name is required and must be at least 2 characters!"
        if len(form["adopt_email"]) < 2:
            errors["adopt_email"] = "Email is required and must be at least 2 characters!"
        if len(form["adopt_address"]) < 2:
            errors["adopt_address"] = "Address is required and must be at least 2 characters!"
        if len(form["adopt_city"]) < 2:
            errors["adopt_city"] = "City is required and must be at least 2 characters!"
        if len(form["adopt_state"]) != 2:
            errors["adopt_state"] = "State is required and must be 2 characters!"
        if len(form["adopt_zipcode"]) != 5:
            errors["adopt_zipcode"] = "Zip Code is required and must be 5 characters!"
        if len(form['home']) < 3:
            errors['home'] = "Home description must be provided and consist of at least 3 characters!"
        if len(form["other_pets"]) < 3:
            errors["other_pets"] = "Other pets information must be provided and consist of at least 3 characters!"   
        if len(form["children"]) < 3:
            errors["children"] = "Children information must be provided and consist of at least 3 characters!"  
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_affiliation = models.CharField(max_length=100)
    user_email = models.CharField(max_length=150)
    user_address = models.CharField(max_length=150)
    user_city = models.CharField(max_length=50)
    user_state = models.CharField(max_length=2)
    user_zipcode = models.IntegerField()
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Pet(models.Model):
    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    sex = models.CharField(max_length=1)
    pet_city = models.CharField(max_length=50)
    pet_state = models.CharField(max_length=2)
    pet_zip_code = models.IntegerField()
    pet_affiliation = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(null= True, blank=True, upload_to="images/")
    status = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    user_fav = models.ManyToManyField(User, related_name="fav_pets")
    user_adopt = models.ManyToManyField(User, related_name="user_adopts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PetManager()

class Adopt(models.Model):
    adopt_fname = models.CharField(max_length=100)
    adopt_lname = models.CharField(max_length=100)
    adopt_email = models.CharField(max_length=150)
    adopt_address = models.CharField(max_length=150)
    adopt_city = models.CharField(max_length=50)
    adopt_state = models.CharField(max_length=2)
    adopt_zipcode = models.IntegerField()
    home = models.TextField()
    other_pets = models.CharField(max_length=50)
    children = models.CharField(max_length=50)
    pet_adopt = models.ManyToManyField(User, related_name="pet_adopts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdoptManager()