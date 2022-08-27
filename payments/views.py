from email import message
from django.shortcuts import render
import logging
from celery import shared_task
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from events.forms import TicketForm
from events.models import Event, Ticket
from django.shortcuts import redirect




@shared_task
def go_to_gateway_view(request,data):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = data['amount']
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = data['user_mobile_number']  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.IDPAY) # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback_gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        # add bank_record to ticket
        ticket = data['ticket']
        ticket.bank_record = bank_record.id
        ticket.save()
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        return render(request, 'failed.html', {'message': e})


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        message = {
            'message': 'این لینک معتبر نیست.'
        }
        return render(request, 'failed.html', message)

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        message = {
            'message': 'این لینک معتبر نیست.'
        }
        return render(request, 'failed.html', message)
    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        # بلیط به موقیت تغییر کرده و به صفحه نتیجه هدایت می شود.
        ticket: Ticket = Ticket.objects.get(bank_record=bank_record.id)
        ticket.status = Ticket.STATUS.SUCCESSFUL
        ticket.save()
        ticket.event_capacity_reducer()

        return redirect(reverse('accounts:my-tickets'))

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    message={
        'message':"پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.",
    }
    return render(request, 'failed.html', message)



class  GoTOGateWayView(LoginRequiredMixin,View):
    form_class = TicketForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # check repitition
            event= Event.objects.last()
            try :
                ticket = Ticket.objects.get(event=event,national_code=form.cleaned_data['national_code'],
                status__in = [Ticket.STATUS.PENDING,Ticket.STATUS.SUCCESSFUL])
                if ticket.status == Ticket.STATUS.SUCCESSFUL:
                    return render(request, 'failed.html', {'message': 'شما قبلا به این رویداد تکرار خرید کرده اید.'})
                ticket.user = request.user
                ticket.save()
            except Ticket.DoesNotExist:
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.event = event
                ticket.save()
            data = {
                "amount": ticket.event.price,
                "user_mobile_number": ticket.phone,
                "ticket": ticket
            }
            return go_to_gateway_view(request,data)
            
        else:
            message= {
                'message': 'اطلاعات وارد شده صحیح نیست.'
            }
            return render(request, 'failed.html', message)