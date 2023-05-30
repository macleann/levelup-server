"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        event.organizer = Gamer.objects.get(pk=event.organizer_id)
        event.game = Game.objects.get(pk=event.game_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()
        for event in events:
            event.organizer = Gamer.objects.get(pk=event.organizer_id)
            event.game = Game.objects.get(pk=event.game_id)
            event.joined = gamer in event.attendees.all()

        if "game" in request.query_params:
            events = events.filter(game_id=request.query_params['game'])

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game_id=request.data["game_id"],
            organizer_id=gamer.id
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game_id = Game.objects.get(pk=request.data["game_id"])
        event.game_id = game_id
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer
    """
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')

class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializers for event game
    """
    class Meta:
        model = Game
        fields = ('id', 'title')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    organizer = EventOrganizerSerializer(many=False)
    game = EventGameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer', 'attendees', 'joined')
        depth = 1
