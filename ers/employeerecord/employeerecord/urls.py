"""
URL configuration for employeerecord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .import views, adminviews, empviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin', RedirectView.as_view(url='/admin/', permanent=False)),
    path('base/', views.BASE, name='base'),
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('Dashboard', views.DASHBOARD, name='dashboard'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),

    #Admin Panel
    path('AdminProfile', adminviews.ADMIN_PROFILE, name='admin_profile'),
    path('AdminProfile/update', adminviews.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('AllStudents', adminviews.ALL_EMPLOYEES, name='all_employees'),
    path('AllEmployees', adminviews.ALL_EMPLOYEES),
    path('AllPredictions', adminviews.ALL_PREDICTIONS, name='all_predictions'),
    path('AllPredictions/<int:prediction_id>/outcome/', adminviews.UPDATE_PREDICTION_OUTCOME, name='admin_update_prediction_outcome'),
    path('ViewEmpProfile/<str:id>', adminviews.VIEW_EMP_PROFILE, name='view_emp_profile'),
    path('UpdateEmployeeProfile', adminviews.UPDATE_EMPLOYEES_PROFILE, name='update_emp_profile'),
    path('ViewEmpEducation/<int:admin_id>/', adminviews.VIEW_EMP_EDUCATION, name='view_emp_education'),
    path('UpdateEmployeeEducation', adminviews.UPDATE_EMPLOYEES_EDUCATION, name='update_emp_education'),
    path('ViewEmpExperience/<int:admin_id>/', adminviews.VIEW_EMP_EXPERIENCE, name='view_emp_experience'),
    path('UpdateEmployeeExperience', adminviews.UPDATE_EMPLOYEES_EXPERIENCE, name='update_emp_experience'),
    path('DeleteEmployee/<int:admin_id>/', adminviews.DELETE_EMPLOYEES_DETAILS, name='delete_employee_details'),
    

    #Employee Panel
    path('students/register/', empviews.EMPSIGNUP, name='student_signup'),
    path('empsignup/', empviews.EMPSIGNUP, name='empsignup'),
    path('StudentProfile', empviews.EMP_PROFILE, name='student_profile'),
    path('EmployeeProfile', empviews.EMP_PROFILE, name='emp_profile'),
    path('StudentProfile/update', empviews.EMP_PROFILE_UPDATE, name='student_profile_update'),
    path('EmployeeProfile/update', empviews.EMP_PROFILE_UPDATE, name='emp_profile_update'),
    path('PredictionForm', empviews.PREDICTION_FORM, name='prediction_form'),
    path('PredictionForm/<int:prediction_id>/outcome/', empviews.UPDATE_ACTUAL_OUTCOME, name='update_actual_outcome'),
    path('PredictionHistory', empviews.PREDICTION_HISTORY, name='prediction_history'),
    path('EmployeeEducation', empviews.EMP_EDUCATION, name='emp_education'),
    path('EmployeeExperience', empviews.EMP_EXPERIENCE, name='emp_exp'),
    path('EmployeeEducationView', empviews.EMP_EDUCATION_VIEW, name='emp_education_view'),
    path('EmployeeEducationDetails', empviews.UPDATE_EMPLOYEE_EDUCATIONS, name='update_employeeedu_details'),
    path('EmployeeExperienceView', empviews.EMP_EXPERIENCE_VIEW, name='emp_experience_view'),
    path('EmployeeExperienceDetails', empviews.UPDATE_EMP_EXPERIENCE, name='update_emp_experience'),
   
    
  
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
