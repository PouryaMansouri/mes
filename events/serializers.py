from asyncio import events
from rest_framework import serializers

from events.models import Ticket
from events.tasks import celery_successful_ticket_sms, ticket_sms

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create (self, validated_data):
        try : 
            #check if user buy ticket before with same national code
            national_code = validated_data['national_code']
            events = validated_data['event']
            ticket = Ticket.objects.get(national_code=national_code, event=events)
            raise serializers.ValidationError({'detail': 'برای این کدملی بلیط در این رویداد ثبت شده است'})
        except Ticket.DoesNotExist:
            ticket = Ticket(**validated_data)
            #add who buy ticket
            ticket.user = self.context['request'].user
            ticket.status = Ticket.STATUS.SUCCESSFUL
            ticket.save()
            ticket.event_capacity_reducer()
            ticket_sms(ticket.phone, ticket.national_code)
            
        return ticket
