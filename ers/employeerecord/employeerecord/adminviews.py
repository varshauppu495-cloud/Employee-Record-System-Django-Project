from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from ersapp.models import CustomUser,Employees,empeducation,empexperience
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
User = get_user_model()

login_required(login_url='/')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'admin/admin_profile.html',context)
@login_required(login_url = '/')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('admin_profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'admin/admin_profile.html')


login_required(login_url='/')
def ALL_EMPLOYEES(request):
    emp_list = Employees.objects.all()
    paginator = Paginator(emp_list, 10)  # Show 10 employees per page

    page_number = request.GET.get('page')
    try:
        emplist = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        emplist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        emplist = paginator.page(paginator.num_pages)

    context = {'emplist': emplist,
   }
    return render(request, 'admin/all_employees.html', context)


login_required(login_url='/')
def VIEW_EMP_PROFILE(request,id):    
    emp = Employees.objects.get(id =id)    
    context = {
        
        "emp":emp,
    }
    return render(request,'admin/update_emp_profile.html',context)

def UPDATE_EMPLOYEES_PROFILE(request):
    if request.method == 'POST':
        try:
            empid = request.POST.get('empid')
            emp = Employees.objects.get(admin_id=empid)
            customuser = CustomUser.objects.get(id=empid)
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
            
            messages.success(request, "Employee detail has been updated successfully")
            return redirect('all_employees')
        except:
            messages.error(request, "Failed to update employee detail")
            return redirect('all_employees')  # Redirect to an appropriate page
    return render(request, 'admin/update_emp_profile.html')


login_required(login_url='/')
def VIEW_EMP_EDUCATION(request, admin_id):
    try:
        emp_edu = empeducation.objects.get(empid=admin_id)
        context = {"emp_edu": emp_edu}
        return render(request, 'admin/view_emp_education.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "Education data does not exist for the provided ID.")
        return redirect('all_employees')



login_required(login_url='/')
def UPDATE_EMPLOYEES_EDUCATION(request):
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
        return redirect('all_employees')

    return render(request, 'admin/view_emp_education.html')





def VIEW_EMP_EXPERIENCE(request, admin_id):
    try:
        emp_exp = empexperience.objects.get(empid=admin_id)
        context = {"emp_exp": emp_exp}
        return render(request, 'admin/emp_experience_view.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "Experience data does not exist for the provided ID.")
        return redirect('all_employees') 



login_required(login_url='/')
def UPDATE_EMPLOYEES_EXPERIENCE(request):
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
        
        employee_exp = empexperience.objects.get(empid=employee_id)
        
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
        return redirect('all_employees')

    return render(request, 'emp_exp_view.html')


def DELETE_EMPLOYEES_DETAILS(request, admin_id):
    try:
        emp_edu = empeducation.objects.get(empid=admin_id)
        emp_edu.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        emp_exp = empexperience.objects.get(empid=admin_id)
        emp_exp.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        emp = Employees.objects.get(admin_id=admin_id)
        emp.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        customuser = CustomUser.objects.get(id=admin_id)
        customuser.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    messages.success(request, 'Record Deleted Successfully!!!')

    return redirect('all_employees')