from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .views import home, profile, RegisterView



urlpatterns = [
    
    #  ADMIN LOGIN / LOGOUT --------------------------------------------------------------------------------------------
    path("admin_login/", views.admin_login, name="admin_login"),
    path('admin_logout/', LogoutView.as_view(next_page='home'), name='admin_logout'),
    
    path('register/', RegisterView.as_view(), name='users-register'),
    path('signin_option/', views.signin_option, name='signin_option'),

    # HOME / CONTACT --------------------------------------------------------------------------------------------
    path('', views.home, name="home"), 
    path('contact/', views.contact, name="contact"),
    path('success/', views.success, name="success"),
    #path('pdf_list/', views.pdf_list, name='pdf_list'),
    
    # SERVICES --------------------------------------------------------------------------------------------
    #path('<slug:services>/', views.services_single, name='services_single'),
    
    path('favourites/', views.favourite_list, name='favourite_list'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('subscribe/', views.subscribe, name="subscribe"),
    
    # BLOG --------------------------------------------------------------------------------------------
    path('blog/', views.blog, name="blog"),
    path('tag/<str:blog_tag>/', views.tag_blog, name='tag_blog'),
    path('category/<category>/', views.category, name="category"),
    path("search_results/", views.search_results, name="search_results"),
    # path('<slug:blog>/', views.blog_single, name='blog_single'),
    
    
    # DASHBOARD --------------------------------------------------------------------------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('register/', RegisterView.as_view(), name='users-register'),
    # path('profile/', profile, name='users-profile'),
    
]