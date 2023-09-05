# Generated by Django 4.2.4 on 2023-09-04 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_is_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rental_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]