# Generated by Django 3.2.14 on 2022-07-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
    ]
