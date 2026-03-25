#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Tự động tạo tài khoản Admin (Nếu chưa tồn tại)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'hhkdigital'
email = 'viethoanglor@gmail.com'
password = 'hhkdigital'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully!')
else:
    print(f'Superuser "{username}" already exists.')
EOF
