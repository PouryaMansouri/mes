# Generated by Django 3.2.15 on 2022-08-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220515_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل'),
        ),
    ]