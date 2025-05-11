from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Job
from .models import Application
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'location', 'category']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['user', 'job']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return resume

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return resume