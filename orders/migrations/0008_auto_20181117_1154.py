# Generated by Django 2.0.3 on 2018-11-17 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20181117_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='size',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='toppings',
            field=models.IntegerField(),
        ),
    ]
