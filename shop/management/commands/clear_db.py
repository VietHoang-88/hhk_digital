from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Xóa sạch toàn bộ sản phẩm và danh mục trong cơ sở dữ liệu'

    def handle(self, *args, **kwargs):
        self.stdout.write('Đang xóa toàn bộ sản phẩm và danh mục...')
        
        # Xóa tất cả sản phẩm trước (vì có khóa ngoại Foreign Key)
        Product.objects.all().delete()
        # Xóa tất cả danh mục
        Category.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Đã xóa sạch dữ liệu thành công!'))
