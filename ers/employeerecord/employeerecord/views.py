import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ersapp.ml_utils import build_admin_analytics, build_history_chart
from ersapp.models import CustomUser, PredictionHistory, StudentProfile, SystemActivityLog

User = get_user_model()


def BASE(request):
    return render(request, 'base.html')


@login_required(login_url='/')
def DASHBOARD(request):
    student_count = StudentProfile.objects.count()
    admin_count = CustomUser.objects.filter(user_type='1').count()
    prediction_qs = PredictionHistory.objects.select_related('student', 'student__admin').all()
    prediction_count = prediction_qs.count()
    analytics = build_admin_analytics(prediction_qs)

    context = {
        'student_count': student_count,
        'admin_count': admin_count,
        'prediction_count': prediction_count,
        'activity_logs': SystemActivityLog.objects.select_related('user')[:6],
    }

    if request.user.user_type == '1':
        context['analytics_json'] = json.dumps(analytics)
        context['at_risk_count'] = sum(1 for item in prediction_qs if item.predicted_label == 'At Risk')
    else:
        profile = StudentProfile.objects.filter(admin=request.user).first()
        student_predictions = list(profile.predictions.all()) if profile else []
        context['latest_prediction'] = student_predictions[0] if student_predictions else None
        context['history_chart_json'] = json.dumps(build_history_chart(student_predictions))
    return render(request, 'dashboard.html', context)


def LOGIN(request):
    return render(request, 'login.html')


def doLogout(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Username or password is not valid.')
        return redirect('login')

    messages.error(request, 'Invalid request method')
    return redirect('login')


@login_required(login_url='/')
def CHANGE_PASSWORD(request):
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check is True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password changed successfully')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request, 'Current password is wrong')
            return redirect("change_password")
    return render(request, 'change-password.html')
