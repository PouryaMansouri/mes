import uuid
import pyqrcode
from pyqrcode import QRCode
import jdatetime
from django.core.validators import RegexValidator
from django.db import models

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

from django_jalali.db import models as jmodels
from accounts.models import User
from events import validators

from teams.models import Team
from azbankgateways.models import Bank
from utils import change_jajali_time_to_string

class Event(BaseModel):
    class Meta:
        verbose_name = _('رویداد')
        verbose_name_plural = _('رویداد')

    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        verbose_name=_('تیم میزبان'),
        related_name='home_team_set'
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        verbose_name=_('تیم مهمان'),
        related_name='away_team_set'
    )

    event_time = jmodels.jDateTimeField(
        verbose_name=_('زمان برگزاری'),
        null=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('توضیحات رویداد'),
    )

    image = models.ImageField(
        null=True,
        blank=True,
        default='events/default.jpg',
        upload_to='events',
        verbose_name=_('تصویر رویداد'),
        help_text=_('لطفا تصویری با عرض y و ارتفاع x پیکسل بارگذاری نمایید.')
    )

    total_capacity = models.PositiveIntegerField(
        verbose_name=_('ظرفیت کل')
    )

    remaining_capacity = models.PositiveIntegerField(
        verbose_name=_('ظرفیت باقیمانده'),
    )

    price = models.PositiveIntegerField(
        verbose_name=_('قیمت'),
        help_text=_('قیمت به تومان'),
        default=0,
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name=_('قابل استفاده بودن'),
        help_text=_(
            'زمانی که ظرفیت رویداد به پایان برسد یا ادمین سایت این گزینه را لغو کند، امکان خرید بلیط برای این رویداد غیرفعال خواهد شد.')
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.remaining_capacity = self.total_capacity
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.home_team.name} | {self.away_team.name}'

    @property
    def is_time(self):
        now = jdatetime.datetime.now()
        if now > self.event_time:
            return False
        return True

    @property
    def is_capacity(self):
        if self.remaining_capacity == 0:
            return False
        return True

    @property
    def str_event_time(self) -> str:
        res = change_jajali_time_to_string(self.event_time)
        return res


class Ticket(BaseModel):
    class Meta:
        verbose_name = _('بلیط')
        verbose_name_plural = _('بلیط')

    class STATUS(models.IntegerChoices):
        PENDING = 1, _('در انتظار')
        SUCCESSFUL = 2, _('موفق')
        FAILED = 3, _('ناموفق')

    full_name = models.CharField(
        _('نام و نام خانوادگی'),
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[\u0600-\u06FF\s]+$',
                message=_('لطفا از کیبورد فارسی استفاده کنید.'),
            ),
        ]
    )

    # birth_datetime = jmodels.jDateTimeField(
    #     verbose_name=_('تاریخ تولد'),
    #     null=True,
    #     blank=True,
    # )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name=_('رویداد'),
    )

    phone = models.CharField(
        max_length=14,
        verbose_name=_('شماره موبایل'),
        validators=[RegexValidator(
            regex='^(0)?9\d{9}$',
            message=_('شماره موبایل معتبر نمیباشد!')
        )]
    )

    national_code = models.CharField(
        max_length=10,
        verbose_name=_('کدملی'),
        validators=[validators.validate_iran_national_code]
    )

    is_used = models.BooleanField(
        default=False,
        verbose_name=_('استفاده شده'),
        help_text=_('زمانی که بلیط تحویل ورزشگاه شد، این فیلد باید توسط ادمین تغییر کند.')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name=_('کاربر'),
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        choices=STATUS.choices,
        default=STATUS.PENDING,
        verbose_name=_('وضعیت'),
    )

    qrcode = models.ImageField(
        null=True,
        blank=True,
        upload_to='tickets',
        verbose_name=_('کد QR'),
    )
    bank_record = models.IntegerField(
        verbose_name='شماره رکورد بانک',
        null=True,
        blank=True
    )
    unique_code = models.UUIDField(
        verbose_name=_('کد یکتا'),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )



    def event_capacity_reducer(self):
        self.event.remaining_capacity -= 1
        if self.event.remaining_capacity == 0:
            self.event.is_available = False
        self.event.save()

    def __str__(self):
        return self.full_name
