# Generated by Django 2.0.3 on 2018-11-09 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181107_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('C', 'Cheese'), ('M', 'Mushrooms'), ('G', 'Green Peppers'), ('O', 'Onions')], default='C', max_length=1)),
            ],
        ),
    ]
