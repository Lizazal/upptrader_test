from django.urls import path
from .views import home, page_not_found

urlpatterns = [
    # главная страница
    path('', home, name='home'),
    # несуществующие ссылки
    path('page-not-found/', page_not_found, name='page_not_found'),
]
