from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'employee'),
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Employees(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    gender = models.CharField(max_length=100,default="0")
    empcode = models.CharField(max_length=20)
    empdept = models.CharField(max_length=100,default="0")
    empdesignation = models.CharField(max_length=150,default="0")
    address = models.CharField(max_length=250,default="0")
    joiningdate = models.CharField(max_length=200,default="0")
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"

class empeducation(models.Model):
    empid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    CoursePG =models.CharField(max_length=200,default="0")
    SchoolCollegePG =models.CharField(max_length=200,default="0")
    YearPassingPG =models.CharField(max_length=200,default="0")
    PercentagePG =models.CharField(max_length=200,default="0")
    CourseGra =models.CharField(max_length=200,default="0")
    SchoolCollegeGra =models.CharField(max_length=200,default="0")
    YearPassingGra =models.CharField(max_length=200,default="0")
    PercentageGra =models.CharField(max_length=200,default="0")
    CourseSSC =models.CharField(max_length=200,default="0")
    SchoolCollegeSSC =models.CharField(max_length=200,default="0")
    YearPassingSSC =models.CharField(max_length=200,default="0")
    PercentageSSC =models.CharField(max_length=200,default="0")
    CourseHSC =models.CharField(max_length=200,default="0")
    SchoolCollegeHSC =models.CharField(max_length=200,default="0")
    YearPassingHSC =models.CharField(max_length=200,default="0")
    PercentageHSC =models.CharField(max_length=200,default="0")
    creationdate = models.DateTimeField(auto_now_add=True)

class empexperience(models.Model):
    empid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    Employer1Name =models.CharField(max_length=200,default="0")
    Employer1Designation = models.CharField(max_length=200,default="0")
    Employer1CTC = models.CharField(max_length=200,default="0")
    Employer1WorkDuration =models.CharField(max_length=200,default="0")
    Employer2Name =models.CharField(max_length=200,default="0")
    Employer2Designation =models.CharField(max_length=200,default="0")
    Employer2CTC =models.CharField(max_length=200,default="0")
    Employer2WorkDuration =models.CharField(max_length=200,default="0")
    Employer3Name =models.CharField(max_length=200,default="0")
    Employer3Designation =models.CharField(max_length=200,default="0")
    Employer3CTC =models.CharField(max_length=200,default="0")
    Employer3WorkDuration =models.CharField(max_length=200,default="0")
    creationdate = models.DateTimeField(auto_now_add=True)

