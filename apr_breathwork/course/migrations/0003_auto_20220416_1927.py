# Generated by Django 3.2 on 2022-04-16 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_duration'),
        ('course', '0002_auto_20220415_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinfo',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='products.product'),
        ),
        migrations.AlterField(
            model_name='urls',
            name='class_no',
            field=models.IntegerField(default=0),
        ),
    ]