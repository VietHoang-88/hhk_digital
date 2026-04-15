from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='products/videos/%Y/%m/%d', verbose_name='Video sản phẩm'),
        ),
    ]
