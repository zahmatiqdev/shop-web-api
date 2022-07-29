# Generated by Django 3.2.14 on 2022-07-29 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220728_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.unit'),
        ),
    ]