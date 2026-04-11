from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho các danh mục và sản phẩm'

    def handle(self, *args, **kwargs):
        categories_data = [
            'Điện Thoại Di Động',
            'Máy tính bảng',
            'Laptop',
            'Loa',
        ]

        products_data = {
            'Điện Thoại Di Động': [
                {'name': 'iPhone 15 Pro Max 256GB', 'price': 29990000, 'stock': 50, 'description': 'Màn hình 6.7 inch, chip A17 Pro mạnh mẽ.'},
                {'name': 'Samsung Galaxy S24 Ultra', 'price': 26990000, 'stock': 40, 'description': 'Bút S-Pen tích hợp, camera 200MP.'},
            ],
            'Máy tính bảng': [
                {'name': 'iPad Pro M2 11 inch', 'price': 19990000, 'stock': 30, 'description': 'Chip M2 siêu mạnh, màn hình Liquid Retina.'},
                {'name': 'Samsung Galaxy Tab S9', 'price': 15490000, 'stock': 25, 'description': 'Màn hình Dynamic AMOLED 2X, kháng nước IP68.'},
            ],
            'Laptop': [
                {'name': 'MacBook Air M3 13 inch', 'price': 27990000, 'stock': 20, 'description': 'Thiết kế siêu mỏng, hiệu năng vượt trội với chip M3.'},
                {'name': 'Dell XPS 13 9340', 'price': 34990000, 'stock': 15, 'description': 'Laptop cao cấp, màn hình vô cực OLED.'},
            ],
            'Loa': [
                {'name': 'Marshall Emberton II', 'price': 3990000, 'stock': 100, 'description': 'Loa di động kháng nước, âm thanh 360 độ.'},
                {'name': 'JBL Charge 5', 'price': 3290000, 'stock': 80, 'description': 'Âm thanh JBL Pro Sound, pin lên đến 20 giờ.'},
            ],
        }

        self.stdout.write('Đang tạo dữ liệu...')

        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            if created:
                self.stdout.write(f'Đã tạo danh mục: {cat_name}')
            
            # Thêm sản phẩm cho danh mục này
            if cat_name in products_data:
                for p_info in products_data[cat_name]:
                    product, p_created = Product.objects.get_or_create(
                        name=p_info['name'],
                        category=category,
                        defaults={
                            'slug': slugify(p_info['name']),
                            'price': p_info['price'],
                            'stock': p_info['stock'],
                            'description': p_info['description'],
                            'available': True
                        }
                    )
                    if p_created:
                        self.stdout.write(f'  - Đã thêm sản phẩm: {p_info["name"]}')

        self.stdout.write(self.style.SUCCESS('Hoàn thành việc tạo dữ liệu mẫu!'))
