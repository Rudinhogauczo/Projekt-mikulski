
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

    def __str__(self):
        return f"{self.name} in {self.room}"

class Uprawnieniauzytkownika(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Urzadzenie, on_delete=models.CASCADE)
    can_change_state = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.device} - {'Można zmienić' if self.can_change_state else 'Nie można zmienić'}"