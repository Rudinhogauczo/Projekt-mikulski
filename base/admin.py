from django.contrib import admin

from .models import Pokoj, Uprawnieniauzytkownika, Urzadzenie

admin.site.register(Pokoj)
admin.site.register(Urzadzenie)
admin.site.register(Uprawnieniauzytkownika)