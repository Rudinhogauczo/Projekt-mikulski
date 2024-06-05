from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, admin_dashboard, edit_permissions, user_list_and_add
urlpatterns = [
    path('', CustomLoginView.as_view(), name='url_login'),
    path('user_rooms/', views.user_rooms, name='url_user_rooms'),
    path('room/<int:room_id>/', views.room_detail, name='url_room_detail'),
    path('admin_wybor/', admin_dashboard, name='url_admin_wybor'),
    path('logout/', CustomLogoutView.as_view(), name='url_logout'),
    path('admin_dodawanie_uzytkownikow/', user_list_and_add, name='url_admin_dodawanie_uzytkownikow'),
    path('admin_dodawanie_pokoi/', views.room_management, name='url_admin_dodawanie_pokoi'),
    path('admin_ustawianie_pokoi/', views.dodaj_urzadzenie, name='url_admin_ustawianie_pokoi'),
    path('delete-urzadzenie/<int:pk>/', views.usun_urzadzenie, name='url_delete_urzadzenie'),
    path('delete-pokoj/<int:pk>/', views.usun_pokoj, name='url_usun_pokoj'),
    path('delete_user/<int:user_id>/', views.delete_user, name='url_delete_user'),
    path('edit_permissions/<int:user_id>/', edit_permissions, name='url_edit_permissions'),  
    path('toggle-device-pin-state/<int:device_id>/<str:new_state>/', views.toggle_device_pin_state, name='toggle_device_pin_state'),
]       