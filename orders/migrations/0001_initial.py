# Generated by Django 4.2.1 on 2023-05-16 17:04

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
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')], max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Office', 'Office'), ('Home', 'Home'), ('Carpet', 'Carpet'), ('Window', 'Window'), ('Bathroom', 'Bathroom')], max_length=20)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Posted', 'Posted'), ('Accepted', 'Accepted'), ('Verified', 'Verified'), ('In_progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Posted', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='client_orders', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_date', '-created_date'],
            },
        ),
    ]
