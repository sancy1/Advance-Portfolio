from django.urls import path
from . import views


urlpatterns = [
    path('services/', views.services, name='services'),
    path("services_search_results/", views.services_search_results, name="services_search_results"),
    path('<slug:services>/', views.services_single, name='services_single'),
]