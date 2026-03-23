from django.contrib import admin

from .models import CustomUser, Employees, PredictionHistory, StudentProfile, SystemActivityLog, empeducation, empexperience


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'admin', 'course', 'semester', 'attendance', 'previous_score')
    search_fields = ('student_id', 'admin__username', 'admin__first_name', 'admin__last_name')


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'predicted_label', 'model_used', 'confidence_score', 'predicted_score', 'created_at')
    list_filter = ('predicted_label', 'model_used', 'created_at')
    search_fields = ('student__student_id', 'student__admin__username')


@admin.register(SystemActivityLog)
class SystemActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    search_fields = ('user__username', 'action', 'details')


admin.site.register(Employees)
admin.site.register(empeducation)
admin.site.register(empexperience)
