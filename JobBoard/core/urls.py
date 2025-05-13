from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ApplicationListView
from .views import edit_profile


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('applications/', ApplicationListView.as_view(), name='application_list'), 
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('dashboard/', views.redirect_dashboard, name='dashboard'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('message/<int:applicant_id>/', views.message_applicant, name='message_applicant'),
    path('inbox/', views.inbox, name='inbox'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('applications/withdraw/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('job/<int:job_id>/save/', views.save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs_list, name='saved_jobs'),
    path('edit-employer-profile/', views.edit_employer_profile, name='edit_employer_profile'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)