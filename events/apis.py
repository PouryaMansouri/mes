from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from events.models import Ticket
from events.serializers import TicketSerializer


class TicketAPI(CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated,]
