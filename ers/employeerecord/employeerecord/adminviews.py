import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from ersapp.forms import ActualOutcomeForm, StudentProfileForm
from ersapp.ml_utils import build_admin_analytics
from ersapp.models import CustomUser, PredictionHistory, StudentProfile, SystemActivityLog


def _ensure_admin(request):
    if request.user.user_type != '1':
        messages.error(request, 'Only administrators can access that page.')
        return False
    return True


def _log_action(user, action, details=''):
    SystemActivityLog.objects.create(user=user, action=action, details=details)


@login_required(login_url='/')
def ADMIN_PROFILE(request):
    if not _ensure_admin(request):
        return redirect('dashboard')
    recent_logs = SystemActivityLog.objects.select_related('user')[:8]
    return render(request, 'admin/admin_profile.html', {'user': request.user, 'recent_logs': recent_logs})


@login_required(login_url='/')
def ADMIN_PROFILE_UPDATE(request):
    if not _ensure_admin(request):
        return redirect('dashboard')

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        _log_action(user, 'Admin Profile Update', 'Admin profile details changed')
        messages.success(request, 'Admin profile updated successfully.')
    return redirect('admin_profile')


@login_required(login_url='/')
def ALL_EMPLOYEES(request):
    if not _ensure_admin(request):
        return redirect('dashboard')
    students = StudentProfile.objects.select_related('admin').all().order_by('-created_at')
    at_risk_count = students.filter(previous_score__lt=50).count()
    return render(request, 'admin/all_employees.html', {'student_list': students, 'at_risk_count': at_risk_count})


@login_required(login_url='/')
def VIEW_EMP_PROFILE(request, id):
    if not _ensure_admin(request):
        return redirect('dashboard')
    student = get_object_or_404(StudentProfile.objects.select_related('admin'), id=id)
    form = StudentProfileForm(initial={
        'first_name': student.admin.first_name,
        'last_name': student.admin.last_name,
        'student_id': student.student_id,
        'mobile_number': student.mobile_number,
        'gender': student.gender,
        'date_of_birth': student.date_of_birth,
        'course': student.course,
        'semester': student.semester,
        'guardian_name': student.guardian_name,
        'contact_email': student.contact_email,
        'address': student.address,
        'attendance': student.attendance,
        'study_hours': student.study_hours,
        'previous_score': student.previous_score,
        'assignments_submitted': student.assignments_submitted,
        'extracurricular_score': student.extracurricular_score,
    })
    return render(request, 'admin/update_emp_profile.html', {'student': student, 'form': form})


@login_required(login_url='/')
def UPDATE_EMPLOYEES_PROFILE(request):
    if not _ensure_admin(request):
        return redirect('dashboard')

    if request.method == 'POST':
        student = get_object_or_404(StudentProfile, id=request.POST.get('student_profile_id'))
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = student.admin
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data.get('profile_pic'):
                user.profile_pic = form.cleaned_data['profile_pic']
            user.save()
            for field in form.Meta.fields:
                setattr(student, field, form.cleaned_data[field])
            try:
                student.save()
                _log_action(request.user, 'Student Profile Updated', f'{student.student_id} updated by admin')
                messages.success(request, 'Student profile updated successfully.')
            except IntegrityError:
                messages.error(request, 'Student ID already exists.')
        else:
            messages.error(request, 'Please correct the student form errors.')
    return redirect('all_employees')


@login_required(login_url='/')
def ALL_PREDICTIONS(request):
    if not _ensure_admin(request):
        return redirect('dashboard')
    predictions = PredictionHistory.objects.select_related('student', 'student__admin').all()
    analytics = build_admin_analytics(predictions)
    return render(
        request,
        'admin/all_predictions.html',
        {
            'predictions': predictions,
            'analytics_json': json.dumps(analytics),
        },
    )


@login_required(login_url='/')
def UPDATE_PREDICTION_OUTCOME(request, prediction_id):
    if not _ensure_admin(request):
        return redirect('dashboard')
    prediction = get_object_or_404(PredictionHistory, id=prediction_id)
    if request.method == 'POST':
        form = ActualOutcomeForm(request.POST, instance=prediction)
        if form.is_valid():
            form.save()
            _log_action(request.user, 'Prediction Outcome Updated', f'Prediction #{prediction.id}')
            messages.success(request, 'Prediction outcome updated successfully.')
    return redirect('all_predictions')


@login_required(login_url='/')
def DELETE_EMPLOYEES_DETAILS(request, admin_id):
    if not _ensure_admin(request):
        return redirect('dashboard')
    user = get_object_or_404(CustomUser, id=admin_id)
    student_id = getattr(user, 'student_profile', None).student_id if hasattr(user, 'student_profile') else user.username
    user.delete()
    _log_action(request.user, 'Student Deleted', f'{student_id} removed')
    messages.success(request, 'Student record deleted successfully.')
    return redirect('all_employees')


@login_required(login_url='/')
def VIEW_EMP_EDUCATION(request, admin_id):
    student = get_object_or_404(StudentProfile, admin_id=admin_id)
    return redirect('view_emp_profile', id=student.id)


@login_required(login_url='/')
def UPDATE_EMPLOYEES_EDUCATION(request):
    messages.info(request, 'Student academic indicators are managed through the profile and prediction modules.')
    return redirect('all_employees')


@login_required(login_url='/')
def VIEW_EMP_EXPERIENCE(request, admin_id):
    return redirect('all_predictions')


@login_required(login_url='/')
def UPDATE_EMPLOYEES_EXPERIENCE(request):
    messages.info(request, 'Prediction tracking replaces the old experience module in this student project.')
    return redirect('all_predictions')
