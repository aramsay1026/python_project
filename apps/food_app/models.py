from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['first_name']) < 3:
            errors["name"] = "Name has to be more than 5 characters"
        if len(postData['last_name']) < 3:
            errors['lname'] = "Name has to be more than 3 characters"
        if len(postData['email']) >3:
            try:
                validate_email(postData['email'])
            except ValidationError as e:
                errors['email']="Wrong Email"
        if len(postData['address'])<1:
            errors['address']="Address cannot be left empty"
        if postData['city'] is None:
            errors['city']=" City cannot be empty"
        if len(postData['psw']) < 8:
            errors["psw"] = "Password has to be more than 8 characters"
        if len(postData['cpsw']) < 8:
            errors['cpsw'] = "Password confirmation has to be more than 8 characters"
        if postData['psw']!=postData['cpsw']:
            errors['password']="Password confirmation does not match Password"
        
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    address=models.CharField(max_length=60)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return "<Object name{},lastname {},email{},address{},city{},state{}>".format(self.first_name,self.last_name,self.email_address,self.address,self.city,self.state,)

    objects=UserManager()

class Supplier(models.Model):
    meals_available=models.IntegerField()
    cooked_at=models.DateTimeField()
    use_by=models.DateTimeField()
    users=models.ManyToManyField(User,related_name="suppliers")
    def __repr(self):
        return "<Supplier: meals{} , cooked{},   use_by{}>".format(self.meals_available,self.cooked_at,self.use_by)

class Shelter(models.Model):
  shelter_name=models.CharField(max_length=50)
  meals_required=models.IntegerField()
  users=models.ManyToManyField(User,related_name="shelters")
  def __repr__(self):
    return "<Shelter Object:{} {}>".format(self.shelter_name,self.meals_required)

class Availability(models.Model):
  available_date=models.DateField()
  available_shift=models.CharField(max_length=25)
  volunteers=models.ManyToManyField(User,related_name="availabilities")
  def __repr__(self):
    return "<Availability Object: {} {}>".format(self.available_date,self.available_shift)

class Feedback(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    message_description=models.TextField()

    def __repr__(self):
        return "Message : name {} , email {} , phone {}, message {}".format(self.name,self.email,self.phone,self.message_description)