import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .forms import LoginForm, RoomForm, UrzadzenieForm
from .models import Pokoj, Uprawnieniauzytkownika, Urzadzenie
import RPi.GPIO as GPIO
from django.http import JsonResponse
GPIO.setmode(GPIO.BCM)
def admin_dashboard(request):
    return render(request, 'base/admin_wybor.html')

def toggle_device_pin_state(request, device_id, new_state):
    device = Urzadzenie.objects.get(id=device_id)
    device.state = new_state
    device.save()

    pin_number = device.pin

    GPIO.setup(pin_number, GPIO.OUT)

    GPIO.output(pin_number, new_state)

    return JsonResponse({'success': True, 'new_state': new_state})

class CustomLoginView(LoginView):
    template_name = 'base/logowanie.html'
    authentication_form = LoginForm
    def get_success_url(self) -> str:
        if self.request.user.is_superuser:
            return reverse_lazy('url_admin_wybor')
        elif self.request.user.is_authenticated:
            return reverse_lazy('url_user_rooms')


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('url_login'))
    

def user_list_and_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('url_admin_dodawanie_uzytkownikow')
        else:

            pass

    users = User.objects.exclude(is_superuser=True)
    return render(request, 'base/admin_dodawanie_uzytkownikow.html', {'users': users})

def room_management(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            nazwa_pokoju = form.cleaned_data['nazwa_pokoju']
            opis_pokoju = form.cleaned_data['opis_pokoju']
            Pokoj.objects.create(nazwa=nazwa_pokoju, opis=opis_pokoju)
            return redirect('url_admin_dodawanie_pokoi')
    else:
        form = RoomForm()
    pokoje = Pokoj.objects.all()
    return render(request, 'base/admin_dodawanie_pokoi.html', {'form': form, 'pokoje': pokoje})


def dodaj_urzadzenie(request):
    if request.method == 'POST':
        form = UrzadzenieForm(request.POST)
        if form.is_valid():
            urzadzenie = form.save(commit=False)
            pin = form.cleaned_data['pin']
            urzadzenie.pin = pin
            urzadzenie.save()
            return redirect('url_admin_ustawianie_pokoi') 
    else:
        form = UrzadzenieForm()
    
    urzadzenia = Urzadzenie.objects.all()
    context = {
        'form': form,
        'urzadzenia': urzadzenia
    }
    return render(request, 'base/admin_ustawianie_pokoi.html', context)

def usun_urzadzenie(request, pk):
    urzadzenie = get_object_or_404(Urzadzenie, pk=pk)
    if request.method == 'POST':
        urzadzenie.delete()
        return redirect('url_admin_ustawianie_pokoi') 
    return redirect('url_admin_wybor')  

def usun_pokoj(request, pk):
    pokoj = get_object_or_404(Pokoj, pk=pk)
    if request.method == 'POST':
        pokoj.delete()
        return redirect('url_admin_dodawanie_pokoi') 
    return redirect('url_admin_wybor') 

def edit_permissions(request, user_id):
    user = User.objects.get(id=user_id)
    rooms = Pokoj.objects.all()
    if request.method == 'POST':
        for room in rooms:
            can_change_state = request.POST.get(f'pokoj_{room.id}') == 'on'
            uprawnienie, created = Uprawnieniauzytkownika.objects.get_or_create(user=user, room=room)
            uprawnienie.can_change_state = can_change_state
            uprawnienie.save()
        return redirect('url_admin_dodawanie_uzytkownikow')  # Redirect to a desired view after saving changes

    user_permissions = Uprawnieniauzytkownika.objects.filter(user=user)
    permissions_dict = {uprawnienie.room.id: uprawnienie.can_change_state for uprawnienie in user_permissions}

    context = {
        'user': user,
        'rooms': rooms,
        'permissions_dict': permissions_dict,
    }
    return render(request, 'base/admin_edycja_uprawnien.html', context)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('url_admin_dodawanie_uzytkownikow')
    return render(request, 'base/admin_ustawianie_pokoi.html', {'user': user})

def user_rooms(request):
    user = request.user
    user_permissions = Uprawnieniauzytkownika.objects.filter(user=user, can_change_state=True)
    rooms = [permission.room for permission in user_permissions]

    context = {
        'rooms': rooms
    }
    return render(request, 'base/room_list.html', context)
 

def room_detail(request, room_id):
    room = get_object_or_404(Pokoj, id=room_id)
    devices = Urzadzenie.objects.filter(room=room)

    context = {
        'room': room,
        'devices': devices
    }
    return render(request, 'base/pokoj.html', context)