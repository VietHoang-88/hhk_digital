from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL thân thiện SEO")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Hình ảnh")
    video = models.FileField(upload_to='products/videos/%Y/%m/%d', blank=True, null=True, verbose_name="Video sản phẩm")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá (VNĐ)")
    stock = models.PositiveIntegerField(verbose_name="Số lượng tồn kho")
    specifications = models.JSONField(default=dict, blank=True, verbose_name="Thông số kỹ thuật")
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('vnpay', 'Thanh toán qua VNPay'),
    )
    CITY_CHOICES = (
        ('Hồ Chí Minh', 'TP. Hồ Chí Minh'),
        ('Hà Nội', 'TP. Hà Nội'),
        ('Đà Nẵng', 'TP. Đà Nẵng'),
        ('Hải Phòng', 'TP. Hải Phòng'),
        ('Cần Thơ', 'TP. Cần Thơ'),
        ('Bình Dương', 'Bình Dương'),
        ('Đồng Nai', 'Đồng Nai'),
        ('Long An', 'Long An'),
        ('Khác', 'Tỉnh thành khác'),
    )
    first_name = models.CharField(max_length=100, verbose_name="Họ")
    last_name = models.CharField(max_length=100, verbose_name="Tên")
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại", default="")
    address = models.TextField(verbose_name="Địa chỉ")
    postal_code = models.CharField(max_length=20, verbose_name="Mã bưu điện", blank=True)
    city = models.CharField(max_length=200, choices=CITY_CHOICES, default='Hồ Chí Minh', verbose_name="Thành phố")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    voucher_code = models.CharField(max_length=50, blank=True, verbose_name='Mã voucher')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Giảm giá (VNĐ)')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return max(sum(item.get_cost() for item in self.items.all()) - self.discount_amount, 0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
