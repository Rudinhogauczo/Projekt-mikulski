
from django.db import models
from django.contrib.auth.models import User

class Pokoj(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.CharField(max_length=200, default='Brak')

    def __str__(self):
        return self.nazwa

class Urzadzenie(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Pokoj, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    pin = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.name} in {self.room}"

class Uprawnieniauzytkownika(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Pokoj, on_delete=models.CASCADE, default=1)
    can_change_state = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.room.nazwa}"