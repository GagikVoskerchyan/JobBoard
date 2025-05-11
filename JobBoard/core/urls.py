from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ApplicationListView  # Only if using CBV
from .views import edit_profile


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('applications/', ApplicationListView.as_view(), name='application_list'),  # or use FBV
    path('dashboard/', views.redirect_dashboard, name='dashboard'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)