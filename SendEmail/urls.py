from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLogin,name="userlogin"),
    path('user-dashboard/',views.UserDashboard,name="userdashboard"),
    path('logout/',views.Logout,name="logout"),
    path('user-sendemail-singal/',views.SendSingalEmail,name="sendsingalemail"),
    path('user-sendemail-multiple/',views.SendMultipleEmail,name="sendmultipleemail"),


    path('superadmin/login/', views.AdminLogin,name="adminlogin"),
    path('superadmin-dashboard/',views.SuperadminDashboard,name="superadmindashboard"),
    path('superadmin-dashboard-<int:pk>-<str:action>/',views.SuperadminDashboard,name="superadmindashboard_update_userdata"),
    path("email-logs/",views.EmailLogs,name="emaillogs"),
    path("add-email/",views.AddEmail,name="addemail"),
    path("receivied-email/",views.ReceivedEmailData,name="receivedemaildata")
    
]
 