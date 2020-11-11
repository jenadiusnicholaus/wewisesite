from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


def homepage(request):
    return render(request, template_name='homepage.html')


def my_profile_account_settings(request):
    return render(request, template_name='authentication/profile_account_settings.html')


def users_profile(request):
    return render(request, template_name='authentication/user_profiles.html')


def users_profile_details(request):
    return render(request, template_name='authentication/user_profile_details.html')


def companies(request):
    return render(request, template_name='company/companies.html')


def about_company(reqest):
    return render(reqest, template_name='company/about_company.html')


def company_profile(request):
    return render(request, template_name='company/company_profile.html')


def jobs(request):
    return render(request, template_name='jobs.html')


def job_details(request):
    return render(request, template_name='job_details.html')


def projects(request):
    return render(request, template_name='projects.html')


def project_details(request):
    return render(request, template_name='project_details.html')


def massages(request):
    return render(request, template_name='messages.html')


def forum(request):
    return render(request, template_name='forum.html')


def forum_post_details(request):
    return render(request, template_name='forum_post_details.html')


def signin(request):
    return render(request, template_name='authentication/signin.html')


def help_center(request):
    return render(request, template_name='help_center.html')
