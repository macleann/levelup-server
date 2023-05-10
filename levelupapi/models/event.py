from django.db import models
from .gamer import Gamer

class Event(models.Model):

    description = models.CharField(max_length=255)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='organized_events')
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField(Gamer, related_name='attended_events')

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
