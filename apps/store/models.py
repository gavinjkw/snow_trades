from django.db import models
import re
from datetime import datetime
from django.utils import timezone
import bcrypt
import os
from uuid import uuid4
#from sorl.thumbnail import ImageField, get_thumbnail
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User_manager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        reg_email = User.objects.filter(email=postData['email'])
        print("Reg email", reg_email)

        if len(reg_email) > 0:
            errors["duplicate_email"] = "Email is already in use" 

        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be longer than two characters" 
        
        elif not postData['first_name'].isalpha():
            errors["first_name"] = "First name should be all letters"

        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be longer than two characters" 

        elif not postData['last_name'].isalpha():
            errors["last_name"] = "Last name should be all letters"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email address" 

        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords do not match" 

        if len(postData['password']) < 8:
            errors["password"] = "Password must be 8 characters or more" 

        return errors

    def basic_validator_login(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email']) 
        print("user", user)
        if len(user) < 1:
            errors["login_failed_one"] = "Login failed" 
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["login_email_one"] = "Please add a valid email" 
                print(errors["login_email_one"])
            elif len(postData['password']) < 1:
                errors["login_password_one"] = "Please add a valid password" 
                print(errors["login_password_one"])
            elif not bcrypt.checkpw(postData['password'].encode(), user[0].hashed_pass.encode()):
                    errors["login_failed_one"] = "Login failed" 
                    print(errors["login_failed_one"])
        return errors

    def basic_validator_edit(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email'])
        all_users = User.objects.all()
        
        if postData['email'] == postData['user_actual_email']:
            print("do nothing")
        elif len(user) > 0:
            if user[0] in all_users:
                errors["email_duplicate"] = "Email is in the database" 
                
        if not EMAIL_REGEX.match(postData['email']):
            errors["edit_email"] = "Please add a valid email" 
      
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be longer than two characters" 
        
        elif not postData['first_name'].isalpha():
            errors["first_name"] = "First name should be all letters"

        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be longer than two characters" 

        elif not postData['last_name'].isalpha():
            errors["last_name"] = "Last name should be all letters"
            
        return errors

    def basic_validator_login_admin(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email']) 
        if len(user) < 1:
            errors["login_failed_one"] = "Login failed" 
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["login_email_one"] = "Please add a valid email" 
            elif len(postData['password']) < 1:
                errors["login_password_one"] = "Please add a valid password" 
            elif not bcrypt.checkpw(postData['password'].encode(), user[0].hashed_pass.encode()):
                errors["login_failed_one"] = "Login failed" 
            elif user[0].access_level != 3:
                errors["login_failed_two"] = "Login failed - access level" 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    access_level = models.IntegerField(default=1)
    hashed_pass = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_manager() 

def path_and_rename(instance, filename):
    upload_to = 'item_photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Item_manager(models.Manager):

    def basic_validator(self, postData, postFiles):
        errors = {}
        print(postData)
        if len(postData['make']) < 3:
            errors["make"] = "Make should be longer than two characters" 

        if len(postData['model']) < 3:
            errors["model"] = "Model should be longer than two characters" 

        if len(postData['size']) < 1:
            errors["size"] = "Please include a size"

        if len(postData['price']) < 1:
            errors["price"] = "Please include a price"
        
        
        if 'category' not in postData:
            errors["category"] = "Please include a category"
        
        if 'condition' not in postData:
            errors["condition"] = "Please include a condition"

        if len(postData['desc']) > 300:
            errors["desc"] = "Description should be thes than 300 characters" 

        if len(postData['desc']) < 50:
            errors["desc"] = "Description should be at least 50 characters"
        
        if 'image_one' not in postFiles:
            errors["image"] = "Please include an image"

        return errors

class Item(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name="item_added")
    image_one = models.ImageField(upload_to=path_and_rename, default = 'item_pictures/None/no-img.jpg')
    image_two = models.ImageField(upload_to=path_and_rename, blank=True, default = 'item_pictures/None/no-img.jpg')
    image_three = models.ImageField(upload_to=path_and_rename, blank=True, default = 'item_pictures/None/no-img.jpg')
    objects = Item_manager() 

class Order(models.Model):

    NOTPAID = 0
    PAID = 1
    PARTPAID = 2

    PAYMENT_STATUS = (
    (NOTPAID, 'Not Paid'),
    (PARTPAID, 'Partial Paid'),
    (PAID, 'Paid'),
    )

    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    buyer = models.ForeignKey(User, related_name='user_buyer')
    seller = models.ForeignKey(User, related_name='user_seller')
    items = models.ManyToManyField(Item, related_name="orders")
    payment_status = models.IntegerField(default=NOTPAID, choices=PAYMENT_STATUS, null=False)
    charge_id = models.CharField(default="1", max_length=234)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

