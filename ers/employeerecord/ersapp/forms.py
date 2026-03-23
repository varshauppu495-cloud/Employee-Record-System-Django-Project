from django import forms

from .models import PredictionHistory, StudentProfile


class StudentRegistrationForm(forms.Form):
    pic = forms.ImageField(required=False)
    student_id = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    mobile_number = forms.CharField(max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    course = forms.CharField(max_length=120, required=False)
    semester = forms.CharField(max_length=30, required=False)
    attendance = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    study_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    previous_score = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    assignments_submitted = forms.IntegerField(required=False)
    extracurricular_score = forms.DecimalField(max_digits=5, decimal_places=2, required=False)


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'mobile_number', 'gender', 'date_of_birth',
            'course', 'semester', 'guardian_name', 'contact_email', 'address',
            'attendance', 'study_hours', 'previous_score',
            'assignments_submitted', 'extracurricular_score',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class PredictionInputForm(forms.Form):
    MODEL_CHOICES = [
        ('auto', 'Auto Select'),
        ('logistic_regression', 'Logistic Regression'),
        ('decision_tree', 'Decision Tree'),
        ('random_forest', 'Random Forest'),
        ('knn', 'KNN'),
    ]

    attendance = forms.DecimalField(max_digits=5, decimal_places=2)
    study_hours = forms.DecimalField(max_digits=5, decimal_places=2)
    previous_score = forms.DecimalField(max_digits=5, decimal_places=2)
    assignments_submitted = forms.IntegerField(min_value=0)
    extracurricular_score = forms.DecimalField(max_digits=5, decimal_places=2)
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES)


class ActualOutcomeForm(forms.ModelForm):
    class Meta:
        model = PredictionHistory
        fields = ['actual_outcome', 'actual_score', 'notes']
