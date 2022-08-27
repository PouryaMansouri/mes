from django.urls import path
from .views import GoTOGateWayView

app_name = 'payments'
urlpatterns = [
    path('pay', GoTOGateWayView.as_view(), name='go_to_gateway'),
]
