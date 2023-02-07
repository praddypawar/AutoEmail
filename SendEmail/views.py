
from ast import main
from django.shortcuts import render,redirect,HttpResponse
from .models import SuperAdmin,Users,EmailData,EmailLog,ReceivedEMail
import datetime
from django.core import mail
from django.contrib import messages


#modules
import imaplib
import email
import pandas as pd

from AutoEmails import config

now = datetime.datetime.now()
hour = now.hour

if hour < 12:
    greeting = "Good morning"
elif hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good night"

print(f"{greeting}!")
# for users -----------------------------------------------------------------------------------
def UserLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password,"  => Login.......")
        if userdata := Users.objects.filter(email=email,password=password):
            print("yesss",userdata[0])
            request.session["id"] = userdata[0].pk
            request.session["email"] = userdata[0].email
            request.session["type"] = "user"
            return redirect("userdashboard")
        else:
            print("nooooo")
            return redirect("userlogin")
    return render(request,"login.html")


def SendSingalEmail(request):
    if "id" not in request.session and "email" not in request.session:
        return redirect("userlogin")
    user_data = Users.objects.get(pk=request.session['id'])
    email_data = EmailData.objects.all()
    email_log = EmailLog.objects.all()
    if request.method == "POST":
        email= request.POST.get("email")
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        try:
           
            email_user_data = EmailData.objects.get(pk=int(email))
            if EmailLog.objects.filter(emailid=email_user_data,subject=subject):
                print("existing....")
                messages.warning(request, 'Already Email sent this user')
            else:

                email1 = mail.EmailMessage(
                subject,
                body,
                'djangomailservices@gmail.com',
                [email_user_data.email],)
                email1.send()
                print(email,subject,body,"---------------------")
                EmailLog(sender=user_data,emailid=email_user_data,subject=subject,body=body).save()
                messages.success(request, 'Email sent successfully!')
            return redirect("sendsingalemail")
        except Exception:
            return redirect("sendsingalemail")
    context ={
        "user_data":user_data,
        "greeting":greeting,
        "title":"SendEmail",
        "email_data":email_data,
        "email_log":email_log
    }
    return render(request,"users/sendsingal.html",context)

def SendMultipleEmail(request):
    if "id" not in request.session and "email" not in request.session:
        return redirect("userlogin")
    user_data = Users.objects.get(pk=request.session['id'])
    email_data = EmailData.objects.all()
    email_log = EmailLog.objects.all()

    if request.method == "POST":
        email= request.POST.getlist("email[]")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        # print(email,subject,body)
        filter_email_id = []
        exist_email_id = []
        filter_email_id1 = []
        for i in email:
            email_user_data_check = EmailData.objects.get(pk=int(i))
            print(email_user_data_check.email)
            if EmailLog.objects.filter(emailid=email_user_data_check,subject=subject):
                exist_email_id.append(email_user_data_check.email)
            else:
                filter_email_id.append(email_user_data_check.email)
                filter_email_id1.append(email_user_data_check)
        # print(filter_email_id)
        # print(exist_email_id)
        try:
           
            email1 = mail.EmailMessage(
            subject,
            body,
            'djangomailservices@gmail.com',
            filter_email_id,)
            email1.send()
            print(email,subject,body,"---------------------")
            for j in filter_email_id1:
                EmailLog(sender=user_data,emailid=j,subject=subject,body=body).save()
            if filter_email_id:
                messages.success(request, f'Email sent successfully! ({filter_email_id})')
            if exist_email_id:
                messages.warning(request, f'Already Email sent this user! ({exist_email_id})')
            return redirect("sendmultipleemail")
        except Exception:
            return redirect("sendmultipleemail")
    context ={
        "user_data":user_data,
        "greeting":greeting,
        "title":"SendEmail",
        "email_data":email_data,
        "email_log":email_log
    }
    return render(request,"users/sendmultiple.html",context)


def UserDashboard(request):
    if "id" not in request.session and "email" not in request.session:
        return redirect("userlogin")
    user_data = Users.objects.get(pk=request.session['id'])
    email_data = EmailData.objects.all()
    context ={
        "user_data":user_data,
        "greeting":greeting,
        "title":"UserDashboard",
        "email_data":email_data
    }
    
    if request.method  == "POST":
        uname= request.POST.get("name")
        email= request.POST.get("email")
        number= request.POST.get("number")

        print(uname,email,number)
        EmailData(name=uname,email=email,phone=number).save()
        return redirect("userdashboard")

    return render(request,"users/dashboard.html",context)


def AddEmails(request):
    if "id" not in request.session and "email" not in request.session and "type" in request.session:
        return redirect("userlogin")
    if request.session["type"] not in ["user", "superadmin"]:
        return redirect("userlogin")


def Logout(request):
    if "id" in request.session:
        del request.session["id"]
    if "email" in request.session:
        del request.session["email"]
    if "type" in request.session:
        del request.session["type"]

    return redirect("userlogin")


#### admin            -------------------------------------------------------------

def AdminLogin(request):
    if request.method != "POST":
        return render(request,"superlogin.html")

    email = request.POST.get("email")
    password = request.POST.get("password")
    print(email,password,"  => Login.......")
    if not (userdata := SuperAdmin.objects.filter(email=email, password=password)):
        return redirect("adminlogin")
    print("yesss",userdata[0])
    request.session["id"] = userdata[0].pk
    request.session["email"] = userdata[0].email
    request.session["type"] = "superadmin"
    return redirect("superadmindashboard")


def SuperadminDashboard(request,pk=0,action=None):
    if "id" not in request.session and "email" not in request.session and "type" not in request.session:
        return redirect("adminlogin")
    if request.session["type"] !="superadmin":
        return redirect("adminlogin")

    superadmin_data = SuperAdmin.objects.get(pk=request.session['id'])
    user_data = Users.objects.all()
    email_data = EmailData.objects.all()
    context ={
        "user_data":user_data,
        "greeting":greeting,
        "title":"SuperAdmin-Dashboard",
        "email_data":email_data,
        "superadmin_data":superadmin_data
    }

    if action =="delete" and pk>0:
        print(pk,"---------delete------------")
        Users.objects.get(pk=pk).delete()
        messages.success(request, 'User Deleted.')
        return redirect("superadmindashboard")

    elif action =="update" and pk>0:
        update_data = Users.objects.get(pk=pk)
        if request.method  == "POST":
            print("update....")
            update_data.fname= request.POST.get("fname")
            update_data.lname= request.POST.get("lname")
            update_data.email= request.POST.get("email")
            update_data.password= request.POST.get("password")
            update_data.save()
            messages.success(request, 'User Data updated.')
            return redirect("superadmindashboard")
        context["update_data"]=update_data
        return render(request,"superadmin/dashboard.html",context)

    else:
        if request.method  == "POST":
            fname= request.POST.get("fname")
            lname= request.POST.get("lname")
            email= request.POST.get("email")
            password= request.POST.get("password")
            print(fname,lname,email,password)
            Users(fname=fname,lname=lname,email=email,password=password).save()
            messages.success(request, 'New User Added.')
            return redirect("superadmindashboard")

        return render(request,"superadmin/dashboard.html",context)


def EmailLogs(request):
    if "id" not in request.session and "email" not in request.session and "type" in request.session:
        return redirect("adminlogin")
    if request.session["type"] !="superadmin":
        return redirect("adminlogin")

    superadmin_data = SuperAdmin.objects.get(pk=request.session['id'])
    email_log = EmailLog.objects.all()
    context ={
        "greeting":greeting,
        "title":"SuperAdmin-Dashboard",
        "superadmin_data":superadmin_data,
        "email_log":email_log
    }

    return render(request,"superadmin/emaillog.html",context)



def AddEmail(request):
    if "id" not in request.session and "email" not in request.session and "type" in request.session:
        return redirect("adminlogin")
    if request.session["type"] !="superadmin":
        return redirect("adminlogin")


    superadmin_data = SuperAdmin.objects.get(pk=request.session['id'])
    email_data = EmailData.objects.all()
    context ={
        "greeting":greeting,
        "title":"SuperAdmin-emaildata",
        "superadmin_data":superadmin_data,
        "email_data":email_data
    }
    if request.method  == "POST":
        uname= request.POST.get("name")
        email= request.POST.get("email")
        number= request.POST.get("number")

        print(uname,email,number)
        EmailData(name=uname,email=email,phone=number).save()
        messages.success(request, 'Email Data added.')
        return redirect("addemail")


    return render(request,"superadmin/addemaildata.html",context)




def ReceivedEmailData(request):
    if "id" not in request.session and "email" not in request.session and "type" in request.session:
        return redirect("userlogin")
    #credentials
    
    #select inbox
    config.Login_user.select("INBOX")
    mail_datas= EmailData.objects.all()
    for i in mail_datas:
        # _, selected_mails = config.Login_user.search(None, f'(FROM "{i.email}")')
        _, selected_mails = config.Login_user.search(None, f'(UNSEEN FROM "{i.email}")')
        print(selected_mails,"=============")
        #total number of mails from specific user
        # print("Total Messages from noreply@kaggle.com:" , len(selected_mails[0].split()))
        for num in selected_mails[0].split():
            _, data = config.Login_user.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            print("bytes_data",bytes_data)
            email_message = email.message_from_bytes(bytes_data)
            print("email_message",email_message)
            msg= ''
            for part in email_message.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    message = part.get_payload(decode=True)
                    msg +=message.decode()
                    break

            yields_df = pd.to_datetime(email_message["date"], infer_datetime_format=True)
            print(yields_df,"=======================")
            # print(ReceivedEMail.objects.values("date").get(pk=7))
            if not ReceivedEMail.objects.filter(emailid=i.email,date=yields_df,subject=email_message["subject"]):
                ReceivedEMail(name=str(email_message["from"]).split("<")[0].replace('"', ''),emailid=i.email,subject=email_message["subject"],body=msg,date=yields_df).save()
    recevied_email_data = ReceivedEMail.objects.all().order_by('-pk')
    
    context ={
        "greeting":greeting,
        "recevied_email_data":recevied_email_data,
    }

    if request.session["type"] == "superadmin":
        superadmin_data = SuperAdmin.objects.get(pk=request.session['id'])
        context["superadmin_data"]=superadmin_data
        context["title"]="SuperAdmin-emaildata"
        return render(request,"superadmin/receivedemail.html",context)

    elif request.session["type"] =="user":
        user_data = Users.objects.get(pk=request.session['id'])
        context["user_data"]=user_data
        context["title"]="user-emaildata"
        return render(request,"users/receivedemail.html",context)
    
    

