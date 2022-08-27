from django.urls import path

from events.apis import TicketAPI
from events.views import Index,PrintTickets

app_name = 'events'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('buy-ticket/', TicketAPI.as_view(), name='buy-ticket'),
    path('ticket-api', TicketAPI.as_view(), name='ticket-api'),
    path('print-ticket/', PrintTickets.as_view(), name='print-ticket'),
]
