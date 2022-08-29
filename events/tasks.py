from celery import shared_task
from kavenegar import KavenegarAPI, APIException, HTTPException

from site_settings.models import SiteSetting

#
@shared_task
def celery_successful_ticket_sms(phone, national_code):
    site_setting = SiteSetting.load()
    print(national_code)
    print(phone)
    # if site_setting and site_setting.kavenegar_sender and site_setting.kavenegar_api_key:
    try:
        api = KavenegarAPI(site_setting.kavenegar_api_key)
        params = {
            'sender': site_setting.kavenegar_sender,
            'receptor': f'{phone}',
            'message': f'سلام هوادار گرامی\nبلیط شما برای بازی مس-ملوان با کدملی {national_code} در تاریخ ۵ اردیبهشت رزرو گردید.\nلطفا در هنگام ورود کارت ملی و کارت واکسن همراه داشته باشید.\nاز ورود شما بدون کارت واکسن جلوگیری میشود.',
        }
        response = api.sms_send(params)
        # todo: uncomment upper line
        # print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

@shared_task
def ticket_sms(phone, national_code):
    site_setting = SiteSetting.load()
    print(national_code)
    print(phone)
    # if site_setting and site_setting.kavenegar_sender and site_setting.kavenegar_api_key:
    try:
        api = KavenegarAPI(site_setting.kavenegar_api_key)
        params = {
            'sender': site_setting.kavenegar_sender,
            'receptor': f'{phone}',
            'message': f'سلام هوادار گرامی\nبلیط شما برای بازی مس-گل گهرسیرجان با کدملی {national_code} در تاریخ 8 شهریور رزرو گردید.\nلطفا در هنگام ورود بلیت همراه داشته باشید.\nاز ورود شما بدون کارت واکسن جلوگیری میشود.',
        }
        response = api.sms_send(params)
        # todo: uncomment upper line
        # print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
