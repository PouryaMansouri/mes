from cProfile import label
from django import forms

from events.models import Ticket, Event


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['full_name', 'phone', 'national_code','user']

        widgets = {
                'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'نام و نام خانوادگی'}),
                'phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'شماره موبایل'}),
                'national_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'کدملی'}),
                'user': forms.HiddenInput(),
            }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'phone': 'شماره موبایل',
            'national_code': 'کدملی',
            'user': 'کاربر',
        }



