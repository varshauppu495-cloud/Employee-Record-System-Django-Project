import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeerecord.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'adminpass123'

u = User.objects.filter(username=username).first()
if u:
    u.set_password(password)
    u.save()
    print('PASSWORD_RESET')
else:
    User.objects.create_superuser(username=username, email='admin@example.com', password=password)
    print('SUPERUSER_CREATED')
