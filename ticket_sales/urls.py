"""ticket_sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from azbankgateways.urls import az_bank_gateways_urls
from payments.views import callback_gateway_view,go_to_gateway_view,GoTOGateWayView

urlpatterns = [
                path('admin/', admin.site.urls),
                #   path('rosetta/', include('rosetta.urls')),
                path('bankgateways/', az_bank_gateways_urls()),
                path('', include('events.urls', namespace='events')),
                path('accounts/', include('accounts.urls', namespace='accounts')),
                path('callback-gateway/', callback_gateway_view, name='callback_gateway'),
                path('go-to-gateway/', include('payments.urls', namespace='payments')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# TODO: static url

admin.site.site_header = "پنل مدیریتی باشگاه مس کرمان"
admin.site.site_title = "باشگاه مس"
admin.site.index_title = "باشگاه مس"
