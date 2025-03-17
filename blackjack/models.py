from django.db import models
from django.contrib.auth.models import User
from datetime import date

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    highest_bet = models.IntegerField(default=0)
    biggest_win = models.IntegerField(default=0)
    biggest_loss = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)  

    def win_rate(self):
        total_games = self.total_wins + self.total_losses
        return (self.total_wins / total_games * 100) if total_games > 0 else 0

    def __str__(self):
        return self.user.username

class TransactionHistory(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.user.username} - {self.transaction_type} ({self.amount})"