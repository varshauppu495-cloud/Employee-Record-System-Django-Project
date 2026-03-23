import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from ersapp.forms import ActualOutcomeForm, PredictionInputForm, StudentProfileForm, StudentRegistrationForm
from ersapp.ml_utils import build_history_chart, build_prediction_chart, predict_student_performance
from ersapp.models import CustomUser, PredictionHistory, StudentProfile, SystemActivityLog


def _log_action(user, action, details=''):
    SystemActivityLog.objects.create(user=user, action=action, details=details)


def _student_profile_defaults(user):
    return {
        'student_id': f"STU{user.id:04d}",
        'mobile_number': '',
        'gender': '',
        'course': '',
        'semester': '',
        'guardian_name': '',
        'contact_email': user.email,
        'address': '',
        'attendance': 0,
        'study_hours': 0,
        'previous_score': 0,
        'assignments_submitted': 0,
        'extracurricular_score': 0,
    }


def _get_or_create_profile(user):
    profile, _ = StudentProfile.objects.get_or_create(
        admin=user,
        defaults=_student_profile_defaults(user),
    )
    return profile


def EMPSIGNUP(request):
    form = StudentRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        try:
            if CustomUser.objects.filter(email=data['email']).exists():
                messages.warning(request, 'Email already exists.')
                return redirect('student_signup')
            if CustomUser.objects.filter(username=data['username']).exists():
                messages.warning(request, 'Username already exists.')
                return redirect('student_signup')
            if StudentProfile.objects.filter(student_id=data['student_id']).exists():
                messages.warning(request, 'Student ID already exists.')
                return redirect('student_signup')

            user = CustomUser(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                user_type='2',
                profile_pic=data.get('pic'),
            )
            user.set_password(data['password'])
            user.save()

            StudentProfile.objects.create(
                admin=user,
                student_id=data['student_id'],
                mobile_number=data.get('mobile_number') or '',
                course=data.get('course') or '',
                semester=data.get('semester') or '',
                contact_email=data['email'],
                attendance=data.get('attendance') or 0,
                study_hours=data.get('study_hours') or 0,
                previous_score=data.get('previous_score') or 0,
                assignments_submitted=data.get('assignments_submitted') or 0,
                extracurricular_score=data.get('extracurricular_score') or 0,
            )
            _log_action(user, 'Student Registration', f"New student account created: {data['student_id']}")
            messages.success(request, 'Student registration completed successfully.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Unable to create the student account.')

    return render(request, 'employee/emp_reg.html', {'form': form})


@login_required(login_url='/')
def EMP_PROFILE(request):
    profile = _get_or_create_profile(request.user)
    form = StudentProfileForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'student_id': profile.student_id,
        'mobile_number': profile.mobile_number,
        'gender': profile.gender,
        'date_of_birth': profile.date_of_birth,
        'course': profile.course,
        'semester': profile.semester,
        'guardian_name': profile.guardian_name,
        'contact_email': profile.contact_email,
        'address': profile.address,
        'attendance': profile.attendance,
        'study_hours': profile.study_hours,
        'previous_score': profile.previous_score,
        'assignments_submitted': profile.assignments_submitted,
        'extracurricular_score': profile.extracurricular_score,
    })
    return render(request, 'employee/emp_profile.html', {'student': profile, 'form': form})


@login_required(login_url='/')
def EMP_PROFILE_UPDATE(request):
    profile = _get_or_create_profile(request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data.get('profile_pic'):
                user.profile_pic = form.cleaned_data['profile_pic']
            user.save()

            for field in form.Meta.fields:
                setattr(profile, field, form.cleaned_data[field])
            try:
                profile.save()
                _log_action(user, 'Profile Update', f'Updated profile for {profile.student_id}')
                messages.success(request, 'Student profile updated successfully.')
            except IntegrityError:
                messages.error(request, 'Student ID must be unique.')
        else:
            messages.error(request, 'Please correct the profile form errors.')
    return redirect('student_profile')


@login_required(login_url='/')
def PREDICTION_FORM(request):
    profile = _get_or_create_profile(request.user)
    latest_prediction = profile.predictions.first()
    chart_image = None
    form = PredictionInputForm(initial={
        'attendance': profile.attendance,
        'study_hours': profile.study_hours,
        'previous_score': profile.previous_score,
        'assignments_submitted': profile.assignments_submitted,
        'extracurricular_score': profile.extracurricular_score,
        'model_choice': 'auto',
    })

    if request.method == 'POST':
        form = PredictionInputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.attendance = data['attendance']
            profile.study_hours = data['study_hours']
            profile.previous_score = data['previous_score']
            profile.assignments_submitted = data['assignments_submitted']
            profile.extracurricular_score = data['extracurricular_score']
            profile.save()

            prediction = predict_student_performance(data, data['model_choice'])
            latest_prediction = PredictionHistory.objects.create(
                student=profile,
                predicted_label=prediction['label'],
                model_used=prediction['model_name'],
                confidence_score=prediction['confidence'],
                predicted_score=prediction['score'],
                attendance=profile.attendance,
                study_hours=profile.study_hours,
                previous_score=profile.previous_score,
                assignments_submitted=profile.assignments_submitted,
                extracurricular_score=profile.extracurricular_score,
                notes='Generated from current academic indicators and selected ML model.',
            )
            chart_image = build_prediction_chart(data, prediction['score'])
            _log_action(request.user, 'Prediction Generated', f"{profile.student_id} using {prediction['model_name']}")
            messages.success(request, 'Performance prediction generated successfully.')
        else:
            messages.error(request, 'Please correct the prediction form errors.')

    if latest_prediction and not chart_image:
        chart_image = build_prediction_chart({
            'attendance': latest_prediction.attendance,
            'study_hours': latest_prediction.study_hours,
            'previous_score': latest_prediction.previous_score,
            'assignments_submitted': latest_prediction.assignments_submitted,
            'extracurricular_score': latest_prediction.extracurricular_score,
        }, latest_prediction.predicted_score)

    outcome_form = ActualOutcomeForm(instance=latest_prediction) if latest_prediction else None
    return render(
        request,
        'employee/prediction_form.html',
        {
            'student': profile,
            'form': form,
            'latest_prediction': latest_prediction,
            'chart_image': chart_image,
            'outcome_form': outcome_form,
        },
    )


@login_required(login_url='/')
def UPDATE_ACTUAL_OUTCOME(request, prediction_id):
    prediction = get_object_or_404(PredictionHistory, id=prediction_id, student__admin=request.user)
    if request.method == 'POST':
        form = ActualOutcomeForm(request.POST, instance=prediction)
        if form.is_valid():
            form.save()
            _log_action(request.user, 'Actual Outcome Updated', f'Prediction #{prediction.id}')
            messages.success(request, 'Actual outcome updated successfully.')
    return redirect('prediction_form')


@login_required(login_url='/')
def PREDICTION_HISTORY(request):
    profile = _get_or_create_profile(request.user)
    predictions = profile.predictions.all()
    history_chart = build_history_chart(predictions)
    return render(
        request,
        'employee/prediction_history.html',
        {
            'student': profile,
            'predictions': predictions,
            'history_chart_json': json.dumps(history_chart),
        },
    )


@login_required(login_url='/')
def EMP_EDUCATION(request):
    return redirect('prediction_form')


@login_required(login_url='/')
def EMP_EXPERIENCE(request):
    return redirect('prediction_history')


@login_required(login_url='/')
def EMP_EDUCATION_VIEW(request):
    return redirect('prediction_form')


@login_required(login_url='/')
def UPDATE_EMPLOYEE_EDUCATIONS(request):
    return redirect('prediction_form')


@login_required(login_url='/')
def EMP_EXPERIENCE_VIEW(request):
    return redirect('prediction_history')


@login_required(login_url='/')
def UPDATE_EMP_EXPERIENCE(request):
    return redirect('prediction_history')
