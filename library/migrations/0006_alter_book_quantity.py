# Generated by Django 4.2.4 on 2023-09-05 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_book_rental_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
