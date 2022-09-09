from django.shortcuts import render
from api.models import Login
from api.models import Signup
from api.models import Admin
from api.models import Car
from api.models import Bike
from api.models import Mobile
from api.models import Laptop
from api.models import Furniture
from api.models import Favorites
from api.models import ChatMessage
from api.models import ChatList
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import check_password
from django.http.response import JsonResponse
from django.conf import settings 
from django.core.mail import send_mail 
import string 
import random 
import base64
from django.core.files.base import ContentFile
# import twilio

import os
# from twilio.rest import Client


# Create your views here.

def home(request):
    return render(request,'index.html')

# @csrf_exempt
# def sendOtp(request):
#     if request.method == 'POST':
#         account_sid = 'AC0249096f2d4a66ebf590a62ad136600e'
#         auth_token = '57e4589013aea22137f6b7fdddcce5c0'
#         client = Client(account_sid, auth_token)

#         otp =  random.randint(1000,9999)

#         #Your new Phone Number is +14078907287
#         message = client.messages.create(
#             body= str(otp) + "\nThis is your one time password(OTP). Do not share with anyone.",
#             from_='+14078907287',
#             to= "+91" + request.POST.get('phone number')
#             )
#         print(message.sid)


@csrf_exempt
def signup_Home(request):
    if request.method =='POST':
        Useremail = request.POST.get('user_email')
        Username = request.POST.get('user_name')
        Userphone = request.POST.get('user_phone')
        Password = request.POST.get('user_password')
        if not Signup.objects.filter(email = Useremail).exists():
            obj = Signup(email = Useremail,name = Username, phone = Userphone, password = Password )
            obj.save()
            return HttpResponse("Saved")
        else :
            return HttpResponse("User Already Exists")

@csrf_exempt
def log(request):
    if request.method =='POST':
        Useremail = request.POST.get('user_email')
        Password = request.POST.get('user_password')
        if Signup.objects.filter(email = Useremail).exists():
            if (Signup.objects.get(email = Useremail).password) == Password:
                data = {
                        'message': 'Login Successfull',
                        'email': Signup.objects.get(email = Useremail).email,
                        'name': Signup.objects.get(email = Useremail).name,
                        'phone': Signup.objects.get(email = Useremail).phone,
                        'password': Signup.objects.get(email = Useremail).password
                        }
                return JsonResponse(data)
                # return HttpResponse("Login Successful") + JsonResponse(list(Signup.objects.get(email = Useremail)))
            else:
                return HttpResponse("Incorrect username or password")
        else:
            return HttpResponse("User does not exist")

@csrf_exempt
def changePassword(request):
    if request.method == 'POST':
        Useremail = request.POST.get('user_email')
        Password = request.POST.get('user_password')
        obj = Signup.objects.get(email = Useremail)
        obj.password = Password
        obj.save()
        return HttpResponse("Password Changed")

@csrf_exempt
def sendHiMail(request):
    if request.method =='POST':
        Useremail = request.POST.get('user_email')
        Username = request.POST.get('user_name')
        subject = 'Welcome to BechDaal App'
        message = f'Hi {Username},This is Manali from Bechdaal Team. Thank you for registering in BechDaal App'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [Useremail, ] 
        send_mail( subject, message, email_from, recipient_list ) 
        return HttpResponse("Mail Sent")

@csrf_exempt
def passwordResetLink(request):
    if request.method =='POST':
        Useremail = request.POST.get('user_email')
        subject = 'Password Reset Request'
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7)) 
        message = f'We have generated a new Password for you \nNew Password: {res}\n\n\nWe recommend you to change it after your login'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [Useremail] 
        send_mail( subject, message, email_from, recipient_list ) 
        obj = Signup.objects.get(email = Useremail)
        obj.password = res
        obj.save()
        return HttpResponse("Password reset Request Recieved, Check your MailBox")
    else:
        return HttpResponse("Something went wrong")

@csrf_exempt
def adminLogin(request):
    if request.method =='POST':
        Id = request.POST.get('admin_id')
        Pass = request.POST.get('secret_code')
        if Admin.objects.filter(adminid = Id).exists():
            if (Admin.objects.get(adminid = Id).password) == Pass:
                adminData = {
                    'message': 'Login Successfull',
                    'adminid': Admin.objects.get(adminid = Id).adminid,
                    'name': Admin.objects.get(adminid = Id).name,
                    'email': Admin.objects.get(adminid = Id).email,
                    'phone': Admin.objects.get(adminid = Id).phone,
                    'password': Admin.objects.get(adminid = Id).password
                }
                return JsonResponse(adminData)
            else:
                return HttpResponse("Invalid Admin ID or password")
        else:
            return HttpResponse("Admin does not exist")

def flatten_dict(dd, separator ='_', prefix =''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

@csrf_exempt
def showAllUsers(request):
    if request.method == 'POST':
        data = {}

        for Name in Signup.objects.raw('Select * from api_signup'):
            key = Name.name
            data[key] = {
                'Name':Name.name,
                'Email':Name.email,
                'Phone':Name.phone
                }
        print(data)
        # return HttpResponse(data)
        return JsonResponse(data)
        # ab = Signup.objects.all()
        # print(Signup.objects.all())
        # return JsonResponse(Signup.objects.all())

# def base64_to_image(base64_string):
#     format, imgstr = base64_string.split(';base64,')
#     ext = format.split('/')[-1]
#     return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)

@csrf_exempt
def uploadCar(request):
    if request.method == 'POST':
        Brand = request.POST.get('brand')
        YearOfRegistration = request.POST.get('yor')
        Model = request.POST.get('model')
        Variant = request.POST.get('variant')
        StateOfRegistration = request.POST.get('sor')
        Owners = request.POST.get('owners')
        KmDriven = request.POST.get('km')
        Fuel = request.POST.get('fuel')
        Transmission = request.POST.get('transmission')
        Features = request.POST.get('features')
        Details = request.POST.get('details')
        ImageStr = request.POST.get('image')
        Price = request.POST.get('price')
        Location = request.POST.get('location')
        Name = request.POST.get('name')
        Phone = request.POST.get('phone')
        Email = request.POST.get('email')
        ref = Signup.objects.get(email=Email)
        # Image = base64_to_image(ImageStr)
        # print(Image)
        obj = Car(brand=Brand, year_of_registration= YearOfRegistration, model= Model, variant= Variant, 
        state_of_registration= StateOfRegistration, no_of_owners = Owners, kms_driven= KmDriven, 
        fuel= Fuel, transmission= Transmission,features= Features, details= Details, 
        image=ImageStr ,price=Price, location = Location, name= Name, phone= Phone, 
        email=ref).save()
        
        return HttpResponse("Saved")
    else:
        return HttpResponse("Error in saving product")

@csrf_exempt
def uploadBike(request):
    if request.method == 'POST':
        BikeType = request.POST.get('bike_type')
        Brand = request.POST.get('brand')
        Year = request.POST.get('year')
        Model = request.POST.get('model')
        KmDriven = request.POST.get('km')
        Features = request.POST.get('features')
        Details = request.POST.get('details')
        ImageStr = request.POST.get('image')
        Price = request.POST.get('price')
        Location = request.POST.get('location')
        Name = request.POST.get('name')
        Phone = request.POST.get('phone')
        Email = request.POST.get('email')
        ref = Signup.objects.get(email=Email)
        # Image = base64_to_image(ImageStr)
          
        obj = Bike(biketype=BikeType,brand=Brand, year= Year, model= Model, kms_driven= KmDriven,features= Features,
        details= Details, image=ImageStr ,price=Price, location = Location, name= Name, phone= Phone, 
        email=ref)
        obj.save()
        return HttpResponse("Saved")

@csrf_exempt
def uploadMobile(request):
    if request.method == 'POST':
        MobileType = request.POST.get('mobile_type')
        Brand = request.POST.get('brand')
        Year = request.POST.get('year')
        Model = request.POST.get('model')
        Features = request.POST.get('features')
        Details = request.POST.get('details')
        ImageStr = request.POST.get('image')
        Price = request.POST.get('price')
        Location = request.POST.get('location')
        Name = request.POST.get('name')
        Phone = request.POST.get('phone')
        Email = request.POST.get('email')
        ref = Signup.objects.get(email=Email)
        # Image = base64_to_image(ImageStr)
        # print(Image)
        obj = Mobile(mobiletype=MobileType,brand=Brand, year= Year, model= Model,features= Features,
        details= Details, image=ImageStr ,price=Price, location = Location, name= Name, phone= Phone, 
        email=ref)
        obj.save()
        return HttpResponse("Saved")

@csrf_exempt
def uploadLaptop(request):
    if request.method == 'POST':
        LaptopType = request.POST.get('laptop_type')
        Brand = request.POST.get('brand')
        Year = request.POST.get('year')
        Model = request.POST.get('model')
        Features = request.POST.get('features')
        Details = request.POST.get('details')
        ImageStr = request.POST.get('image')
        Price = request.POST.get('price')
        Location = request.POST.get('location')
        Name = request.POST.get('name')
        Phone = request.POST.get('phone')
        Email = request.POST.get('email')
        ref = Signup.objects.get(email=Email)
        # Image = base64_to_image(ImageStr)
        # print(Image)
        obj = Laptop(laptoptype=LaptopType, brand=Brand, year= Year, model= Model,features= Features,
        details= Details, image=ImageStr ,price=Price, location = Location, name= Name, phone= Phone, 
        email=ref)
        obj.save()
        return HttpResponse("Saved")



@csrf_exempt
def uploadFurniture(request):
    if request.method == 'POST':
        FurnitureType = request.POST.get('furniture_type')
        Brand = request.POST.get('brand')
        Year = request.POST.get('year')
        Model = request.POST.get('model')
        Features = request.POST.get('features')
        Details = request.POST.get('details')
        ImageStr = request.POST.get('image')
        Price = request.POST.get('price')
        Location = request.POST.get('location')
        Name = request.POST.get('name')
        Phone = request.POST.get('phone')
        Email = request.POST.get('email')
        ref = Signup.objects.get(email=Email)
        # Image = base64_to_image(ImageStr)
        # print(ImageStr)
        obj = Furniture(furnituretype=FurnitureType, features= Features, details= Details, image=ImageStr ,
        price=Price, location = Location, name= Name, phone= Phone, email=ref)
        obj.save()
        return HttpResponse("Saved")

@csrf_exempt
def showImage(request):
    if request.method == 'POST':
        link = Car.objects.get(email="manaligandhi2000@gmail.com").image
        print(link.name)
        return HttpResponse(link.name)

@csrf_exempt
def viewProduct(request):
    if request.method == 'POST':
        Text = request.POST.get("text")
        email = request.POST.get("email")
        data = {}
        if Text == "Car > Cars":
            for element in Car.objects.raw("Select * from api_car"):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)
        if Text == 'Car > Hardware & tools':
            for element in Car.objects.raw("Select * from api_car"):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                   'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)
        if Text == 'Car > View All':
            for element in Car.objects.raw("Select * from api_car"):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  
        if Text == 'Car':
            for element in Car.objects.raw("Select * from api_car"):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  
        if Text == 'Bike > With Gear':
            for element in Bike.objects.raw('Select * from api_bike where biketype="Motorcycle"'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)
        if Text == 'Bike > W/O Gear':
            for element in Bike.objects.raw('Select * from api_bike where biketype="Scooty"'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)   
        if Text == 'Bike':
            for element in Bike.objects.raw('Select * from api_bike'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  
        if Text == 'Mobile':
            for element in Mobile.objects.raw('Select * from api_mobile'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  
        if Text == 'Laptop':
            for element in Laptop.objects.raw('Select * from api_laptop'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.model,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  
        if Text == 'Furniture':
            for element in Furniture.objects.raw('Select * from api_furniture'):
                if Favorites.objects.filter(email = email, pid = element).exists():
                    fav = "Yes"
                else:
                    fav = "No"
                data[str(element)] = {
                    'model': element.furnituretype,
                    'price': element.price,
                    'image': str(element.image),
                    'pId': str(element),
                    'fav': fav
                }
            return JsonResponse(data)  

@csrf_exempt
def randomProducts(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        num = random.randint(1,9)
        print(num)
        prod= {}
        for i in range(0,num):
            carPid = Car.objects.order_by('?').first()
            if Favorites.objects.filter(email = email, pid = carPid).exists():
                fav = "Yes"
            else:
                fav = "No"
            prod[str(carPid)] = {
                "Image": str(carPid.image),
                "Product Name": carPid.model,
                "Product Price": carPid.price,
                "Product Id": str(carPid),
                "Favorite": fav
            }
            bikePid = Bike.objects.order_by('?').first()
            if Favorites.objects.filter(email = email, pid = bikePid).exists():
                fav = "Yes"
            else:
                fav = "No"
            prod[str(bikePid)] = {
                "Image": str(bikePid.image),
                "Product Name": bikePid.model,
                "Product Price": bikePid.price,
                "Product Id": str(bikePid),
                "Favorite": fav
            }
            mobilePid = Mobile.objects.order_by('?').first()
            if Favorites.objects.filter(email = email, pid = mobilePid).exists():
                fav = "Yes"
            else:
                fav = "No"
            prod[str(mobilePid)] = {
                "Image":str(mobilePid.image),
                "Product Name": mobilePid.model,
                "Product Price": mobilePid.price,
                "Product Id": str(mobilePid),
                "Favorite": fav
            }
            laptopPid = Laptop.objects.order_by('?').first()
            if Favorites.objects.filter(email = email, pid = laptopPid).exists():
                fav = "Yes"
            else:
                fav = "No"
            prod[str(laptopPid)] = {
                "Image":str(laptopPid.image),
                "Product Name": laptopPid.model,
                "Product Price": laptopPid.price,
                "Product Id": str(laptopPid),
                "Favorite": fav
            }
            furniturePid = Furniture.objects.order_by('?').first()
            if Favorites.objects.filter(email = email, pid = furniturePid).exists():
                fav = "Yes"
            else:
                fav = "No"
            prod[str(furniturePid)] = {
                "Image":str(furniturePid.image),
                "Product Name": furniturePid.furnituretype,
                "Product Price": furniturePid.price,
                "Product Id": str(furniturePid),
                "Favorite": fav
            }
        return JsonResponse(prod)

@csrf_exempt
def addFavorites(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pid = request.POST.get('pid')
        if not Favorites.objects.filter(email = email, pid = pid).exists():
            obj = Favorites(email = email, pid= pid)
            obj.save()
            return HttpResponse("Added to Favorite")
        else :
            return HttpResponse("Already Favorite")

@csrf_exempt
def removeFavorite(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pid = request.POST.get('pid')
        Favorites.objects.get(email = email, pid = pid).delete()
        return HttpResponse("Removed from Favorite")

@csrf_exempt
def favProducts(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        data = {}
        for element in Favorites.objects.raw('Select * from api_favorites where email = %s',[email]):
            if str(element.pid).startswith('CAR'):
                value = str(element.pid).split("CAR",1)[-1]
                product = Car.objects.get(p_id=value)
                data[str(product)] = {
                    "Image":str(product.image),
                    "Product Name": product.model,
                    "Product Price": product.price,
                    "Product Id": str(product),
                    "Favorite": "Yes"
                }
            elif str(element.pid).startswith('BIKE'):
                value = str(element.pid).split("BIKE",1)[-1]
                product = Bike.objects.get(p_id=value)
                data[str(product)] = {
                    "Image":str(product.image),
                    "Product Name": product.model,
                    "Product Price": product.price,
                    "Product Id": str(product),
                    "Favorite": "Yes"
                }
            elif str(element.pid).startswith('MOBILE'):
                value = str(element.pid).split("MOBILE",1)[-1]
                product = Mobile.objects.get(p_id=value)
                data[str(product)] = {
                    "Image":str(product.image),
                    "Product Name": product.model,
                    "Product Price": product.price,
                    "Product Id": str(product),
                    "Favorite": "Yes"
                }
            elif str(element.pid).startswith('LAPTOP'):
                value = str(element.pid).split("LAPTOP",1)[-1]
                product = Laptop.objects.get(p_id=value)
                data[str(product)] = {
                    "Image":str(product.image),
                    "Product Name": product.model,
                    "Product Price": product.price,
                    "Product Id": str(product),
                    "Favorite": "Yes"
                }
            elif str(element.pid).startswith('FURNITURE'):
                value = str(element.pid).split("FURNITURE",1)[-1]
                product = Furniture.objects.get(p_id=value)
                data[str(product)] = {
                    "Image":str(product.image),
                    "Product Name": product.furnituretype,
                    "Product Price": product.price,
                    "Product Id": str(product),
                    "Favorite": "Yes"
                }

        return JsonResponse(data)

@csrf_exempt
def viewSpecificProduct(request):
    if request.method =='POST':
        pid = request.POST.get("pid")
        data = {}
        if pid.startswith('CAR'):
            val = pid.split("CAR",1)[-1]
            product = Car.objects.get(p_id=val)
            data[str(product)] = {
                "Image":str(product.image),
                "Name": product.model,
                "Price": product.price,
                "Brand": product.brand,
                "Variant": product.variant,
                "Location": product.location,
                "Features": product.features,
                "Description": product.details,
                "Year of Registration": product.year_of_registration,
                "State of Registration": product.state_of_registration,
                "Kilometers Driven": product.kms_driven,
                "No. of Owners": product.no_of_owners,
                "Fuel": product.fuel,
                "Transmission Type": product.transmission,
                "Phone": product.phone,
                "Seller Name": product.name,
                "Id": str(product)
            }
        elif pid.startswith('BIKE'):
            val = pid.split("BIKE",1)[-1]
            product = Bike.objects.get(p_id=val)
            data[str(product)] = {
                "Image":str(product.image),
                "Name": product.model,
                "Price": product.price,
                "Brand": product.brand,
                "Location": product.location,
                "Features": product.features,
                "Description": product.details,
                "Year": product.year,
                "Kilometers Driven": product.kms_driven,
                "Phone": product.phone,
                "Seller Name": product.name,
                "Id": str(product)
            }
        elif pid.startswith('MOBILE'):
            val = pid.split("MOBILE",1)[-1]
            product = Mobile.objects.get(p_id=val)
            data[str(product)] = {
                "Image":str(product.image),
                "Name": product.model,
                "Price": product.price,
                "Brand": product.brand,
                "Location": product.location,
                "Features": product.features,
                "Description": product.details,
                "Year": product.year,
                "Phone": product.phone,
                "Seller Name": product.name,
                "Id": str(product)
            }
        elif pid.startswith('LAPTOP'):
            val = pid.split("LAPTOP",1)[-1]
            product = Laptop.objects.get(p_id=val)
            data[str(product)] = {
                "Image":str(product.image),
                "Name": product.model,
                "Price": product.price,
                "Brand": product.brand,
                "Location": product.location,
                "Features": product.features,
                "Description": product.details,
                "Year": product.year,
                "Phone": product.phone,
                "Seller Name": product.name,
                "Id": str(product)
            }
        elif pid.startswith('FURNITURE'):
            val = pid.split("FURNITURE",1)[-1]
            product = Furniture.objects.get(p_id=val)
            data[str(product)] = {
                "Image":str(product.image),
                "Name": product.furnituretype,
                "Price": product.price,
                "Location": product.location,
                "Features": product.features,
                "Description": product.details,
                "Phone": product.phone,
                "Seller Name": product.name,
                "Id": str(product)
            }
        return JsonResponse(data)

@csrf_exempt
def loadChat(request):
    if request.method == 'POST':
        Sender = request.POST.get("sender")
        Reciever = request.POST.get("reciever")
        texts = []
        for element in ChatMessage.objects.raw("Select * from api_chatmessage where (sender = %s and reciever = %s) or (sender = %s and reciever = %s) order by time ASC;",[Sender,Reciever,Reciever,Sender]):
            if element.sender == Sender:
                txt = "Sender "+str(element.message)
                texts.append(txt)
            elif element.sender == Reciever:
                txt = "Reciever "+str(element.message)
                texts.append(txt)
        chat={}
        chat["Chat"]= texts
        return JsonResponse(chat)

@csrf_exempt
def saveChat(request):
    if request.method == 'POST':
        Sender = request.POST.get("sender")
        Reciever = request.POST.get("reciever")
        Message = request.POST.get("message")
        Name = request.POST.get("name")
        if not ChatList.objects.filter(user1=Sender,user2= Reciever).exists():
            ChatList(user1=Sender,user2=Reciever,user2Name=Name).save()
        obj = ChatMessage(sender= Sender, reciever= Reciever, message= Message)
        obj.save()
        return HttpResponse("Saved")

@csrf_exempt
def chatNameList(request):
    if request.method =='POST':
        MyUsername = request.POST.get("myusername")
        nameList = {}
        for a in ChatList.objects.raw("Select * from api_chatlist where user1 = %s",[MyUsername]):
            nameList[str(a.user2)] = a.user2Name
        return JsonResponse(nameList)
