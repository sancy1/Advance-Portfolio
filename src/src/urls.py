
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from App.views import CustomLoginView, ResetPasswordView, ChangePasswordView, blog_single,  profile, users_dashboard
from App.forms import LoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    #path('accounts/', include('allauth.urls')),
    path('services/', include(("services.urls", 'services'), namespace="services")),
    
    
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    
    path('social/', include('social_django.urls', namespace='social')),
    
    path('users_dashboard/', users_dashboard, name='users_dashboard'),
    path('profile/', profile, name='users-profile'),
    path('<slug:blog>/', blog_single, name='blog_single'),

]

#handler404 = 'App.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)