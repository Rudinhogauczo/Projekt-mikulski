from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import CustomLoginView, CustomLogoutView, admin_dashboard, change_device_state, user_list_and_add
urlpatterns = [
    path('', CustomLoginView.as_view(), name='url_login'),
    path('base/', login_required(views.room_list), name='room_list'),  
    path('room/<int:room_id>/', views.device_list, name='device_list'),
    path('device/<int:device_id>/change/', change_device_state, name='change_device_state'),
    path('admin_wybor/', admin_dashboard, name='url_admin_wybor'),
    path('logout/', CustomLogoutView.as_view(), name='url_logout'),
    path('admin_dodawanie_uzytkownikow/', user_list_and_add, name='url_admin_dodawanie_uzytkownikow'),
    path('admin_dodawanie_pokoi/', views.room_management, name='url_admin_dodawanie_pokoi'),
    path('admin_ustawianie_pokoi/', views.dodaj_urzadzenie, name='url_admin_ustawianie_pokoi'),
    path('delete-urzadzenie/<int:pk>/', views.usun_urzadzenie, name='url_delete_urzadzenie'),
    path('delete-pokoj/<int:pk>/', views.usun_pokoj, name='url_usun_pokoj'),
]