#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput
# Lệnh xóa sạch dữ liệu cũ bị lỗi ảnh (Lưu ý: Bạn nên xóa dòng này sau khi dữ liệu đã sạch)
python manage.py clear_db

# Tạo Superuser mặc định (tk/mk: hhkdigital)
export DJANGO_SUPERUSER_USERNAME=hhkdigital
export DJANGO_SUPERUSER_PASSWORD=hhkdigital
export DJANGO_SUPERUSER_EMAIL=admin@hhkdigital.com
python manage.py createsuperuser --no-input || true
