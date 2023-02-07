"""AutoEmails URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
import imaplib
import email
import pandas as pd
from . import config

print("hello............................")
username ="youremail"
    #generated app password
app_password= "password"
# https://www.systoolsgroup.com/imap/
gmail_host= 'imap.gmail.com'
#set connection
config.Login_user = imaplib.IMAP4_SSL(gmail_host,993)
#login
config.Login_user.login(username, app_password)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("SendEmail.urls")),
]
