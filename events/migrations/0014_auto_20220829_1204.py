# Generated by Django 3.2.15 on 2022-08-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_ticket_national_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'در انتظار'), (2, 'موفق'), (3, 'ناموفق')], default=2, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='unique_code',
            field=models.CharField(blank=True, max_length=230, null=True, verbose_name='کد یکتا'),
        ),
    ]
