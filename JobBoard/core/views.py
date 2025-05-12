from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.models import User


from .forms import RegisterForm, JobForm, ApplicationForm, ProfileForm, MessageForm
from .models import Job, Application, Profile
from .models import EmployerProfile, SeekerProfile
from .models import Message  # add this import


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'core/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

def home_view(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html')

def home_view(request):
    jobs = Job.objects.all().order_by('-date_posted')
    return render(request, 'core/job_list.html', {'jobs': jobs})

def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user  # ✅ FIX HERE
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, 'core/job_detail.html', {'job': job, 'form': form})


def application_list_view(request):
    applications = Application.objects.all().order_by('-applied_at')
    return render(request, 'core/application_list.html', {'applications': applications})

def job_apply_view(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        application = Application(
            user=request.user,
            job=job,
            name=request.POST['name'],
            email=request.POST['email'],
        )
        application.save()
        return redirect('application_list')  # Redirect to applications page
    return render(request, 'core/job_apply.html', {'job': job})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 👇 Temporarily attach user_type for signal
            user.user_type = form.cleaned_data.get('user_type')
            user.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def landing_page(request):
    return render(request, 'core/landing_page.html')  # create this template

def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'core/profile.html', {'form': form})

@login_required
def post_job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()
    return render(request, 'core/post_job.html', {'form': form})

@login_required
def redirect_dashboard(request):
    try:
        profile = request.user.profile
        if profile.user_type == 'seeker':
            return redirect('seeker_dashboard')
        elif profile.user_type == 'employer':
            return redirect('employer_dashboard')
        else:
            return redirect('home')  # fallback
    except Exception as e:
        print("Redirect error:", e)
        return redirect('home')  # avoid infinite loop

@login_required
def seeker_dashboard(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'dashboard/seeker_dashboard.html', {'applications': applications})

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'dashboard/employer_dashboard.html', {'jobs': jobs})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or redirect to profile
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/edit_profile.html', {'form': form})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    application.delete()
    return redirect('application_list')


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = Application.objects.filter(job=job)
    return render(request, 'core/view_applicants.html', {'job': job, 'applicants': applicants})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == 'POST':
        job.delete()
        return redirect('employer_dashboard')

    return render(request, 'jobs/delete_job.html', {'job': job})

@login_required
def message_applicant(request, applicant_id):
    applicant = get_object_or_404(User, id=applicant_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']

            Message.objects.create(
                sender=request.user,
                recipient=applicant,
                subject=subject,
                body=body,
            )

            messages.success(request, "Message sent!")
            return redirect('employer_dashboard')
    else:
        form = MessageForm()

    return render(request, 'applications/message_applicant.html', {'form': form, 'applicant': applicant})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'messages/inbox.html', {'messages': messages})
