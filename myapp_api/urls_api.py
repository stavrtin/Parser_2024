from django.urls import path
from .views import home  # Импортируем вашу функцию представления

urlpatterns = [
    path('', home, name='home'),  # Указываем корневой маршрут для функции home
]