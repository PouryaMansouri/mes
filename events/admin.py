from core.admin import BaseAdmin
from events.models import Event, Team, Ticket
from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


class EventAdmin(BaseAdmin):
    list_filter = (
        ('event_time', JDateFieldListFilter),
    )


class TicketAdmin(BaseAdmin):
    list_display = ['event', 'full_name', 'phone', 'national_code', 'user','bank_record','status','unique_code']

    search_fields = ['full_name', 'phone', 'national_code']


    list_filter = ['status']


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
