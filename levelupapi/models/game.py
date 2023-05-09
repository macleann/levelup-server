from django.db import models


class Game(models.Model):

    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    skill_level = models.CharField(max_length=50)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='game_types')
    creator = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='created_games')
