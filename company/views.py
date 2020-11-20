import hashlib
import hmac
import os

from django.contrib import messages
from django.shortcuts import render, redirect
from validate_email import validate_email

from .forms import CompanyForm
from .models import Company

# Create your views here.
from django.views.generic.base import View


def get_salt():
    salt = os.urandom(16)
    return salt


def get_hashed_password(password):
    """  hash password on company register"""
    password = password.encode()
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)

    return password_hash


def verify_password(password):
    """ validate the password on  company login"""
    encoded__password = hashlib.pbkdf2_hmac("sha256", password.encode(), get_salt(), 100000)
    is_valid=hmac.compare_digest(get_hashed_password(password), encoded__password)
    return is_valid


class CompanySignUp(View):

    def post(self, request, *args, **kwargs):
        form = CompanyForm(self.request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            company_email = form.cleaned_data.get('company_email')
            country = form.cleaned_data.get('country')
            password1 = form.cleaned_data.get('password2')
            password2 = form.cleaned_data.get('password2')
            agreed = request.POST.get('agreed')
            if not validate_email(company_email):
                messages.error(request, 'enter validemail address')
            if agreed:
                if password1 == password2:
                    new_company = Company()
                    new_company.company_name = company_name
                    new_company.country = country
                    new_company.company_email = company_email
                    new_company.password1 = get_hashed_password(password1)
                    new_company.agreed_to_terms = True
                    new_company.save()

                    # authenticate the company so that to able to login in the future
                    # comp_auth=c()

                    messages.info(self.request, f"welcome home{company_name}")
                    return redirect('/')
                else:
                    messages.info(self.request, "password doesn't much")
                    return redirect('/')

            else:
                messages.info(self.request, 'show your really consent')
                return redirect('/')
        print(form.data)
        messages.warning(self.request, 'form is invalid')
        return redirect('/')


