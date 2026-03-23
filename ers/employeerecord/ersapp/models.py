from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'employee'),
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='profile_pic', default='profile_pic/user.png', blank=True)


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


class StudentProfile(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=120, blank=True)
    semester = models.CharField(max_length=30, blank=True)
    guardian_name = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    attendance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    study_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    previous_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assignments_submitted = models.PositiveIntegerField(default=0)
    extracurricular_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.admin.get_full_name() or self.admin.username}"


class PredictionHistory(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='predictions')
    predicted_label = models.CharField(max_length=50)
    model_used = models.CharField(max_length=50, default='Auto')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    predicted_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    attendance = models.DecimalField(max_digits=5, decimal_places=2)
    study_hours = models.DecimalField(max_digits=5, decimal_places=2)
    previous_score = models.DecimalField(max_digits=5, decimal_places=2)
    assignments_submitted = models.PositiveIntegerField(default=0)
    extracurricular_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    actual_outcome = models.CharField(max_length=50, blank=True)
    actual_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.predicted_label}"


class SystemActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    details = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else 'system'
        return f"{username} - {self.action}"

