import email
from urllib import request
from django.db import models

# Create your models here.
class Base(models.Model):
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class SuperAdmin(Base):
    email = models.EmailField()
    password = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.email


class Users(Base):
    fname = models.CharField(max_length=210)
    lname = models.CharField(max_length=210)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def  __str__(self):
        return self.fname


class EmailData(Base):
    name = models.CharField(max_length=210)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name



class EmailLog(Base):
    sender = models.ForeignKey(Users,on_delete=models.PROTECT)
    emailid = models.ForeignKey(EmailData,on_delete=models.PROTECT)
    subject = models.CharField(max_length=255)
    body = models.CharField(max_length=255)

    def __str__(self):
        return self.emailid.email

    
class ReceivedEMail(Base):
    name = models.CharField(max_length=210)
    emailid = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    date = models.DateTimeField()


    def __str__(self) -> str:
        return self.emailid


