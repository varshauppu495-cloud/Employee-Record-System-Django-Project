import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeerecord.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()
matches = list(User.objects.filter(Q(username__icontains='varsha') | Q(first_name__icontains='varsha') | Q(email__icontains='varsha')))
if not matches:
    print('USER_NOT_FOUND')
else:
    for u in matches:
        u.is_staff = True
        u.save()
        print(f'PROMOTED:{u.username}')
