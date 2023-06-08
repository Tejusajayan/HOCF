# Generated by Django 4.2.2 on 2023-06-08 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='dinereq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('number', models.PositiveBigIntegerField()),
                ('datetime', models.DateTimeField()),
                ('seat', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodname', models.CharField(max_length=40)),
                ('foodprice', models.PositiveIntegerField()),
                ('cate', models.CharField(max_length=30)),
                ('foodimg', models.ImageField(upload_to='FOODS')),
                ('special', models.BooleanField(default=False)),
                ('avai', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Customer Name')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('status', models.CharField(default='PENDING', max_length=254, verbose_name='Payment Status')),
                ('provider_order_id', models.CharField(max_length=40, verbose_name='Order ID')),
                ('payment_id', models.CharField(max_length=36, verbose_name='Payment ID')),
                ('signature_id', models.CharField(max_length=128, verbose_name='Signature ID')),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='finalord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.PositiveIntegerField(default=0)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('bill', models.PositiveIntegerField(default=0)),
                ('payment', models.CharField(max_length=30)),
                ('paymentid', models.CharField(default='-', max_length=50)),
                ('paydone', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=30)),
                ('number', models.PositiveBigIntegerField(default=0)),
                ('doorno', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=100)),
                ('pincode', models.PositiveIntegerField(default=0)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HOME.customer')),
            ],
        ),
        migrations.CreateModel(
            name='cartitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('orderid', models.CharField(max_length=10)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HOME.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HOME.food')),
            ],
        ),
    ]