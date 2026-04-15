from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_add_product_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='voucher_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='Mã voucher'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=0, verbose_name='Giảm giá (VNĐ)'),
        ),
    ]
