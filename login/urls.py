"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views
from django.conf.urls.static import static
from login import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('htm/',views.home),
    # path('sendotp',views.sendOtp),
    path('signup',views.signup_Home),
    path('login',views.log),
    path('changepassword',views.changePassword),
    path('sendhimail',views.sendHiMail),
    path('passwordresetlink',views.passwordResetLink),
    path('adminlogin',views.adminLogin),
    path('showallusers',views.showAllUsers),
    path('uploadcar',views.uploadCar),
    path('showimage',views.showImage),
    path('uploadbike',views.uploadBike),
    path('uploadmobile',views.uploadMobile),
    path('uploadlaptop',views.uploadLaptop),
    path('uploadfurniture',views.uploadFurniture),
    path('viewproduct',views.viewProduct),
    path('randomproducts',views.randomProducts),
    path('addfavorites',views.addFavorites),
    path('removefavorite',views.removeFavorite),
    path('favproduct',views.favProducts),
    path('viewspecificproduct',views.viewSpecificProduct),
    path('loadchat',views.loadChat),
    path('savechat',views.saveChat),
    path('chatnamelist',views.chatNameList)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
