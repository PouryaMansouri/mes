# Generated by Django 3.2.15 on 2022-08-17 16:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_ticket_bank_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='unique_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='کد یکتا'),
        ),
    ]
