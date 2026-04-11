from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests
import os

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho các danh mục và sản phẩm có kèm ảnh'

    def handle(self, *args, **kwargs):
        categories_data = [
            'Điện Thoại Di Động',
            'Máy tính bảng',
            'Laptop',
            'Loa',
            'Phụ Kiện',
            'TV Smart',
        ]

        products_data = {
            'Điện Thoại Di Động': [
                {
                    'name': 'iPhone 15 Pro Max 256GB', 
                    'price': 29990000, 
                    'stock': 50, 
                    'description': 'Màn hình 6.7 inch, chip A17 Pro mạnh mẽ.',
                    'image_url': 'https://th.bing.com/th/id/OIP.rkgqD1ZsstYsu7Lzw1PIWQHaFQ?w=288&h=204&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra', 
                    'price': 26990000, 
                    'stock': 40, 
                    'description': 'Bút S-Pen tích hợp, camera 200MP.',
                    'image_url': 'https://th.bing.com/th/id/OIP.RCaOvi3C_QXx33EUvGht9wHaFj?w=245&h=184&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
            ],
            'Máy tính bảng': [
                {
                    'name': 'iPad Pro M2 11 inch', 
                    'price': 19990000, 
                    'stock': 30, 
                    'description': 'Chip M2 siêu mạnh, màn hình Liquid Retina.',
                    'image_url': 'https://th.bing.com/th/id/OIP.xMM2jSZArKHeWydu-uv38gHaHa?w=172&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'Samsung Galaxy Tab S9', 
                    'price': 15490000, 
                    'stock': 25, 
                    'description': 'Màn hình Dynamic AMOLED 2X, kháng nước IP68.',
                    'image_url': 'https://th.bing.com/th/id/OIP.ELCbKzqe8iiurmk6ewaMgQHaFE?w=261&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
            ],
            'Laptop': [
                {
                    'name': 'MacBook Air M3 13 inch', 
                    'price': 27990000, 
                    'stock': 20, 
                    'description': 'Thiết kế siêu mỏng, hiệu năng vượt trội với chip M3.',
                    'image_url': 'https://th.bing.com/th/id/OIP.q9cWZbW4_eXQDyIa_07X9gHaFj?w=246&h=185&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'Dell XPS 13 9340', 
                    'price': 34990000, 
                    'stock': 15, 
                    'description': 'Laptop cao cấp, màn hình vô cực OLED.',
                    'image_url': 'https://th.bing.com/th/id/OIP.-ScWbeEErL-wWE7PhDmGdQHaEK?w=260&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
            ],
            'Loa': [
                {
                    'name': 'Marshall Emberton II', 
                    'price': 3990000, 
                    'stock': 100, 
                    'description': 'Loa di động kháng nước, âm thanh 360 độ.',
                    'image_url': 'https://th.bing.com/th/id/OIP.JgjWTI8snGZTJzM_OcdijwHaD2?w=279&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'JBL Charge 5', 
                    'price': 3290000, 
                    'stock': 80, 
                    'description': 'Âm thanh JBL Pro Sound, pin lên đến 20 giờ.',
                    'image_url': 'https://tse4.mm.bing.net/th/id/OIP.vrmRdOsqt3SWt9E_uV46IQHaEl?rs=1&pid=ImgDetMain&o=7&rm=3'
                },
            ],
            'Phụ Kiện': [
                {
                    'name': 'Apple Watch Series 9 GPS 41mm', 
                    'price': 9490000, 
                    'stock': 60, 
                    'description': 'Theo dõi sức khỏe, màn hình Always-On siêu sáng.',
                    'image_url': 'https://th.bing.com/th/id/OIP.dQwi9KnaFg47d8sUFE79VAHaIs?w=175&h=206&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'AirPods Pro (2nd generation) MagSafe', 
                    'price': 5790000, 
                    'stock': 120, 
                    'description': 'Chống ồn chủ động, âm thanh không gian cá nhân hóa.',
                    'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MTJV3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1694014871985'
                },
            ],
            'TV Smart': [
                {
                    'name': 'Samsung Crystal UHD 4K 55 inch UA55AU7700', 
                    'price': 12990000, 
                    'stock': 15, 
                    'description': 'Màu sắc sống động, độ phân giải 4K sắc nét.',
                    'image_url': 'https://th.bing.com/th/id/OIP.9NEw4KS_p6PC0U_IFzsztQHaHa?w=206&h=206&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
                {
                    'name': 'Sony BRAVIA XR OLED 65 inch XR-65A80L', 
                    'price': 45990000, 
                    'stock': 10, 
                    'description': 'Màn hình OLED hoàn hảo, âm thanh phát ra từ màn hình.',
                    'image_url': 'https://th.bing.com/th/id/OIP.plxlcahm1jHNYEDvbkJm4wHaE0?w=325&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
                },
            ],
        }

        self.stdout.write('Đang tạo dữ liệu và tải ảnh...')

        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            
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
                        self.stdout.write(f'  - Đang tải ảnh cho: {p_info["name"]}')
                        try:
                            response = requests.get(p_info['image_url'], timeout=10)
                            if response.status_code == 200:
                                file_name = f"{slugify(p_info['name'])}.jpg"
                                product.image.save(file_name, ContentFile(response.content), save=True)
                                self.stdout.write(f'    + Đã tải xong ảnh.')
                        except Exception as e:
                            self.stdout.write(f'    ! Lỗi tải ảnh: {e}')

        self.stdout.write(self.style.SUCCESS('Hoàn thành việc tạo dữ liệu mẫu kèm hình ảnh!'))
