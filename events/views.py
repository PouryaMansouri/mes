from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from events.forms import TicketForm
from events.models import Event, Ticket
from players.models import Player


class Index(FormView):
    form_class = TicketForm
    template_name = 'index.html'
    success_url = reverse_lazy('events:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = Player.objects.order_by('-goal')[:4]
        event = Event.objects.last()
        context['players'] = players
        context['event'] = event
        context['event_date'] = event.str_event_time
        return context


class PrintTickets(View):
    template_name = 'ticket.html'

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket: Ticket = Ticket.objects.get(id=ticket_id)
            context = {
                'name': ticket.full_name,
                'national_code': ticket.national_code,
                'team_a': ticket.event.home_team.name,
                'team_b': ticket.event.away_team.name,
                'date': ticket.event.str_event_time,
                'location': "ورزشگاه مس باهنر کرمان",
                'unique_code': ticket.unique_code,
            }
            return render(request, self.template_name, context)
        except Ticket.DoesNotExist:
            message = 'بلیط مورد نظر یافت نشد'
            return render(request, 'failed.html', {'message': message})
