from django.db import models

class Login(models.Model):
    email=models.CharField(max_length=200,default="email")
    name=models.CharField(max_length=200,default="name")
    phone=models.CharField(max_length=10,default="phone")
    password=models.CharField(max_length=200,default="1234")
    def __unicode__(self):
        return self.name

class Signup(models.Model):
    email=models.CharField(max_length=200,default="email",primary_key=True)
    name=models.CharField(max_length=200,default="name")
    phone=models.CharField(max_length=10,default="phone")
    password=models.CharField(max_length=200,default="1234")
    def __int__(self):
        return self.email


class Car(models.Model):
    p_id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=100,default="brand")
    year_of_registration = models.IntegerField(default="year")
    model = models.CharField(max_length=100,default="model")
    variant = models.CharField(max_length=100,default="variant")
    state_of_registration = models.CharField(max_length=100,default="state")
    no_of_owners = models.CharField(max_length=40,default="owners")
    kms_driven = models.CharField(max_length=200,default="kms_driven")
    fuel = models.CharField(max_length=100,default="fuel")
    transmission = models.CharField(max_length=100,default="transmission")
    features = models.CharField(max_length=200,default="features")
    details = models.CharField(max_length=200,default="details")
    image = models.CharField(max_length=1000000,default="image")
    price = models.IntegerField(default="0")
    location = models.CharField(max_length=200,default="location")
    name = models.CharField(max_length=100,default="name")
    phone = models.CharField(max_length=10,default="phone")
    email = models.ForeignKey(Signup,on_delete=models.CASCADE)
    def __str__(self):
        return "CAR"+str(self.p_id)


class Bike(models.Model):
    p_id = models.IntegerField(primary_key=True)
    biketype = models.CharField(max_length=100,default="biketype")
    brand = models.CharField(max_length=100,default="brand")
    model = models.CharField(max_length=100,default="model")
    year = models.IntegerField(default="year")
    kms_driven = models.CharField(max_length=200,default="kms_driven")
    features = models.CharField(max_length=200,default="features")
    details = models.CharField(max_length=200,default="details")
    image = models.CharField(max_length=1000000,default="image")
    price = models.IntegerField(default="0")
    location = models.CharField(max_length=200,default="location")
    name = models.CharField(max_length=100,default="name")
    phone = models.CharField(max_length=10,default="phone")
    email = models.ForeignKey(Signup,on_delete=models.CASCADE)
    def __str__(self):
        return "BIKE"+str(self.p_id)

class Mobile(models.Model):
    p_id = models.IntegerField(primary_key=True)
    mobiletype = models.CharField(max_length=100,default="mobiletype")
    brand = models.CharField(max_length=100,default="brand")
    model = models.CharField(max_length=100,default="model")
    year = models.IntegerField(default="year")
    features = models.CharField(max_length=200,default="features")
    details = models.CharField(max_length=200,default="details")
    image = models.CharField(max_length=1000000,default="image")
    price = models.IntegerField(default="0")
    location = models.CharField(max_length=200,default="location")
    name = models.CharField(max_length=100,default="name")
    phone = models.CharField(max_length=10,default="phone")
    email = models.ForeignKey(Signup,on_delete=models.CASCADE)
    def __str__(self):
        return "MOBILE"+str(self.p_id)

class Laptop(models.Model):
    p_id = models.IntegerField(primary_key=True)
    laptoptype = models.CharField(max_length=100,default="laptopType")
    brand = models.CharField(max_length=100,default="brand")
    model = models.CharField(max_length=100,default="model")
    year = models.IntegerField(default="year")
    features = models.CharField(max_length=200,default="features")
    details = models.CharField(max_length=200,default="details")
    image = models.CharField(max_length=1000000,default="image")
    price = models.IntegerField(default="0")
    location = models.CharField(max_length=200,default="location")
    name = models.CharField(max_length=100,default="name")
    phone = models.CharField(max_length=10,default="phone")
    email = models.ForeignKey(Signup,on_delete=models.CASCADE)
    def __str__(self):
        return "LAPTOP"+str(self.p_id)

class Furniture(models.Model):
    p_id = models.IntegerField(primary_key=True)
    furnituretype = models.CharField(max_length=100,default="furnitureType")
    features = models.CharField(max_length=200,default="features")
    details = models.CharField(max_length=200,default="details")
    image = models.CharField(max_length=1000000,default="image")
    price = models.IntegerField(default="0")
    location = models.CharField(max_length=200,default="location")
    name = models.CharField(max_length=100,default="name")
    phone = models.CharField(max_length=10,default="phone")
    email = models.ForeignKey(Signup,on_delete=models.CASCADE)
    def __str__(self):
        return "FURNITURE"+str(self.p_id)

class Admin(models.Model):
    adminid=models.CharField(max_length=20)
    email=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=200)
    def __str__(self):
        return self.adminid

class Favorites(models.Model):
    email = models.CharField(max_length=200,default='email')
    pid = models.CharField(max_length = 40,default='0')
    def __str__(self):
        return self.email

class ChatMessage(models.Model):
    sender = models.CharField(max_length=12,default="0123456789")
    reciever = models.CharField(max_length=12,default="9876543210")
    message = models.CharField(max_length=500,default="message")
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.message

class ChatList(models.Model):
    user1 = models.CharField(max_length=12,default="0123456789")
    user2 = models.CharField(max_length=12,default="9876543210")
    user2Name = models.CharField(max_length=40,default="Name")
    def __str__(self):
        return self.user2Name