from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from ersapp.models import CustomUser,Employees,empeducation,empexperience
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
User = get_user_model()

def EMPSIGNUP(request):
   
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')        
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('empsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('empsignup')
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=2,
               profile_pic = pic,
            )
            user.set_password(password)
            user.save()            
            emp = Employees(
                admin = user,                
                mobilenumber = mobno,              
                
            )
            emp.save()            
            messages.success(request,'Signup Successfully')
            return redirect('empsignup')
    
    

    return render(request,'employee/emp_reg.html')

login_required(login_url='/')
def EMP_PROFILE(request):
    
    emp =Employees.objects.get(admin_id =request.user.id)
    
    context = {
        
        "emp":emp,
    }
    return render(request,'employee/emp_profile.html',context)


@login_required(login_url = '/')
def EMP_PROFILE_UPDATE(request):
    if request.method == "POST":
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            emp = Employees.objects.get(admin_id=request.user.id)

            # Update user data
            customuser.first_name = request.POST.get('first_name', customuser.first_name)
            customuser.last_name = request.POST.get('last_name', customuser.last_name)
            if 'profile_pic' in request.FILES:
                customuser.profile_pic = request.FILES['profile_pic']
            customuser.save()

            # Update employee data
            emp.mobilenumber = request.POST.get('mobilenumber', emp.mobilenumber)
            emp.gender = request.POST.get('gender', emp.gender)
            emp.empcode = request.POST.get('empcode', emp.empcode)
            emp.empdept = request.POST.get('empdept', emp.empdept)
            emp.gender = request.POST.get('gender', emp.gender)
            emp.empdesignation = request.POST.get('empdesignation', emp.empdesignation)
            emp.address = request.POST.get('address', emp.address)
            emp.save()

            messages.success(request, "Your profile has been updated successfully")
            return redirect('emp_profile')
        except ObjectDoesNotExist:
            messages.error(request, "User or employee profile not found")
        except IntegrityError:
            messages.error(request, "Employee code must be unique")
            return redirect('emp_profile')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'employee/emp_profile.html')

@login_required(login_url='/')
def EMP_EDUCATION(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.method == "POST":
            # Retrieve the Employees instance associated with the current user
            employee = Employees.objects.get(admin_id=request.user.id)
            custom_user = employee.admin
            # Create an instance of EmpEducation and assign the admin attribute of the Employees instance to the empid field
            empedu = empeducation(
                CoursePG=request.POST.get('CoursePG'),
                SchoolCollegePG=request.POST.get('SchoolCollegePG'),
                YearPassingPG=request.POST.get('YearPassingPG'),
                PercentagePG=request.POST.get('PercentagePG'),
                CourseGra=request.POST.get('CourseGra'),
                SchoolCollegeGra=request.POST.get('SchoolCollegeGra'),
                YearPassingGra=request.POST.get('YearPassingGra'),
                PercentageGra=request.POST.get('PercentageGra'),
                CourseSSC=request.POST.get('CourseSSC'),
                SchoolCollegeSSC=request.POST.get('SchoolCollegeSSC'),
                YearPassingSSC=request.POST.get('YearPassingSSC'),
                PercentageSSC=request.POST.get('PercentageSSC'),
                CourseHSC=request.POST.get('CourseHSC'),
                SchoolCollegeHSC=request.POST.get('SchoolCollegeHSC'),
                YearPassingHSC=request.POST.get('YearPassingHSC'),
                PercentageHSC=request.POST.get('PercentageHSC'),
                empid=custom_user  # Assign the Employees instance to the empid field
            )
            empedu.save()
            messages.warning(request, 'Your education details have been added successfully!!!')
            return redirect("emp_education")
        else:
            # Retrieve existing education details for the current user
            try:
                eedu = empeducation.objects.get(empid=request.user.id)
                context = {'eedu': eedu}
            except empeducation.DoesNotExist:
                context = {}  # If no education details found, pass an empty context
            return render(request, 'employee/myeducation.html', context)
    else:
        messages.error(request, 'You need to login to access this page.')
        return redirect('login')  # Redirect to the login page if the user is not authenticated

        
@login_required(login_url='/')
def EMP_EXPERIENCE(request):
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve the Employees instance associated with the current user
            employee = Employees.objects.get(admin_id=request.user.id)
            # Retrieve the CustomUser instance associated with the Employees instance
            custom_user = employee.admin
            
            # Now create an instance of empexperience and assign the admin attribute of the Employees instance to the empid field
            empexp = empexperience(
                Employer1Name=request.POST.get('Employer1Name'),
                Employer1Designation=request.POST.get('Employer1Designation'),
                Employer1CTC=request.POST.get('Employer1CTC'),
                Employer1WorkDuration=request.POST.get('Employer1WorkDuration'),
                Employer2Name=request.POST.get('Employer2Name'),
                Employer2Designation=request.POST.get('Employer2Designation'),
                Employer2CTC=request.POST.get('Employer2CTC'),
                Employer2WorkDuration=request.POST.get('Employer2WorkDuration'),
                Employer3Name=request.POST.get('Employer3Name'),
                Employer3Designation=request.POST.get('Employer3Designation'),
                Employer3CTC=request.POST.get('Employer3CTC'),
                Employer3WorkDuration=request.POST.get('Employer3WorkDuration'),
                empid=custom_user  # Assign the CustomUser instance to the empid field
            )
            empexp.save()
            messages.warning(request, 'Your experience details have been added successfully!!!')
            return redirect("emp_exp")
    else:
        if request.user.is_authenticated:
            # Retrieve existing experience details for the current user
            try:
                eexp = empexperience.objects.get(empid=request.user.id)
                context = {'eexp': eexp}
            except empexperience.DoesNotExist:
                context = {}  # If no experience details found, pass an empty context
            return render(request, 'employee/myexp.html', context)
        else:
            messages.error(request, 'You need to login to access this page.')
            return redirect('login')
      
  


@login_required(login_url='/')
def EMP_EDUCATION_VIEW(request):
    try:
        emp_edu = empeducation.objects.get(empid_id=request.user.id)
    except empeducation.DoesNotExist:
        # If the education data doesn't exist for the user, set emp_edu to None
        emp_edu = None

    context = {
        "emp_edu": emp_edu,
    }
    return render(request, 'employee/emp_education_view.html', context)

login_required(login_url='/')
def UPDATE_EMPLOYEE_EDUCATIONS(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        CoursePG = request.POST.get('CoursePG')
        SchoolCollegePG = request.POST.get('SchoolCollegePG')
        YearPassingPG = request.POST.get('YearPassingPG')
        PercentagePG = request.POST.get('PercentagePG')
        CourseGra = request.POST.get('CourseGra')
        SchoolCollegeGra = request.POST.get('SchoolCollegeGra')
        YearPassingGra = request.POST.get('YearPassingGra')
        PercentageGra = request.POST.get('PercentageGra')
        CourseSSC = request.POST.get('CourseSSC')
        SchoolCollegeSSC = request.POST.get('SchoolCollegeSSC')
        YearPassingSSC = request.POST.get('YearPassingSSC')
        PercentageSSC = request.POST.get('PercentageSSC')
        CourseHSC = request.POST.get('CourseHSC')
        SchoolCollegeHSC = request.POST.get('SchoolCollegeHSC')
        YearPassingHSC = request.POST.get('YearPassingHSC')
        PercentageHSC = request.POST.get('PercentageHSC')
        
        # Retrieve the employee education object
        employeeedu = empeducation.objects.get(empid_id=employee_id)
        
        # Update the fields
        employeeedu.CoursePG = CoursePG
        employeeedu.SchoolCollegePG = SchoolCollegePG
        employeeedu.YearPassingPG = YearPassingPG
        employeeedu.PercentagePG = PercentagePG
        employeeedu.CourseGra = CourseGra
        employeeedu.SchoolCollegeGra = SchoolCollegeGra
        employeeedu.YearPassingGra = YearPassingGra
        employeeedu.PercentageGra = PercentageGra
        employeeedu.CourseSSC = CourseSSC
        employeeedu.SchoolCollegeSSC = SchoolCollegeSSC
        employeeedu.YearPassingSSC = YearPassingSSC
        employeeedu.PercentageSSC = PercentageSSC
        employeeedu.CourseHSC = CourseHSC
        employeeedu.SchoolCollegeHSC = SchoolCollegeHSC
        employeeedu.YearPassingHSC = YearPassingHSC
        employeeedu.PercentageHSC = PercentageHSC
        
        # Save the changes
        employeeedu.save()
        
        # Add a success message
        messages.success(request, "Education details have been updated successfully")
        
        # Redirect to the view page
        return redirect('emp_education_view')

    return render(request, 'employee/emp_education_view.html')



@login_required(login_url='/')
def EMP_EXPERIENCE_VIEW(request):
    try:
        emp_exp = empexperience.objects.get(empid_id=request.user.id)
    except empexperience.DoesNotExist:
        # If the experience data doesn't exist for the user, set emp_exp to None
        emp_exp = None

    context = {
        "emp_exp": emp_exp,
    }
    return render(request, 'employee/emp_exp_view.html', context)


login_required(login_url='/')
def UPDATE_EMP_EXPERIENCE(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        Employer1Name=request.POST.get('Employer1Name')
        Employer1Designation=request.POST.get('Employer1Designation')
        Employer1CTC=request.POST.get('Employer1CTC')
        Employer1WorkDuration=request.POST.get('Employer1WorkDuration')
        Employer2Name=request.POST.get('Employer2Name')
        Employer2Designation=request.POST.get('Employer2Designation')
        Employer2CTC=request.POST.get('Employer2CTC')
        Employer2WorkDuration=request.POST.get('Employer2WorkDuration')
        Employer3Name=request.POST.get('Employer3Name')
        Employer3Designation=request.POST.get('Employer3Designation')
        Employer3CTC=request.POST.get('Employer3CTC')
        Employer3WorkDuration=request.POST.get('Employer3WorkDuration')
        
        employee_exp = empexperience.objects.get(empid_id=employee_id)
        
        # Update the fields
        employee_exp.Employer1Name=Employer1Name
        employee_exp.Employer1Designation=Employer1Designation
        employee_exp.Employer1CTC=Employer1CTC
        employee_exp.Employer1WorkDuration=Employer1WorkDuration
        employee_exp.Employer2Name=Employer2Name
        employee_exp.Employer2Designation=Employer2Designation
        employee_exp.Employer2CTC=Employer2CTC
        employee_exp.Employer2WorkDuration=Employer2WorkDuration
        employee_exp.Employer3Name=Employer3Name
        employee_exp.Employer3Designation=Employer3Designation
        employee_exp.Employer3CTC=Employer3CTC
        employee_exp.Employer3WorkDuration=Employer3WorkDuration
    
     # Save the changes
        employee_exp.save()
        
        # Add a success message
        messages.success(request, "Experience details have been updated successfully")
        
        # Redirect to the view page
        return redirect('emp_experience_view')

    return render(request, 'employee/emp_exp_view.html')






