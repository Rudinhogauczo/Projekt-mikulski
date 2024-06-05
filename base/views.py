import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .forms import LoginForm, RoomForm, UrzadzenieForm
from .models import Pokoj, Uprawnieniauzytkownika, Urzadzenie


def admin_dashboard(request):
    return render(request, 'base/admin_wybor.html')

class CustomLoginView(LoginView):
    template_name = 'base/logowanie.html'
    authentication_form = LoginForm
    def get_success_url(self) -> str:
        if self.request.user.is_superuser:
            return reverse_lazy('url_admin_wybor')
        elif self.request.user.is_authenticated:
            return reverse_lazy('room_list')


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
            form.save()
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

@login_required
def room_list(request):
    rooms = Pokoj.objects.all()
    return render(request, 'base/room_list.html', {'rooms': rooms})

@login_required
def device_list(request, room_id):
    room = get_object_or_404(Pokoj, id=room_id)
    devices = Urzadzenie.objects.filter(room=room)
    user_permissions = Uprawnieniauzytkownika.objects.filter(user=request.user, device__in=devices)
    permissions_dict = {permission.device.id: permission.can_change_state for permission in user_permissions}
    return render(request, 'base/device_list.html', {'room': room, 'devices': devices, 'permissions_dict': permissions_dict})

@login_required
def change_device_state(request, device_id):
    device = get_object_or_404(Urzadzenie, id=device_id)
    user_permission = Uprawnieniauzytkownika.objects.filter(user=request.user, device=device).first()
    if user_permission and user_permission.can_change_state:
        if request.method == 'POST':
            data = json.loads(request.body)
            new_state = data.get('state')
            device.state = new_state
            device.save()
            return JsonResponse({'message': 'Device state updated successfully'})
    return JsonResponse({'error': 'Permission denied'}, status=403)    
    
