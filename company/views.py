import hashlib
import hmac
import os

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from validate_email import validate_email

from authentication.models import User
from authentication.tokens import account_activation_token
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
    is_valid = hmac.compare_digest(get_hashed_password(password), encoded__password)
    return is_valid


class CompanySignUp(View):

    def post(self, request, *args, **kwargs):
        form = CompanyForm(self.request.POST)
        # if the form is valid we need to grab all information from it
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            company_email = form.cleaned_data.get('company_email')
            country = form.cleaned_data.get('country')
            password1 = form.cleaned_data.get('password2')
            password2 = form.cleaned_data.get('password2')
            agreed = request.POST.get('agreed')
            # checking for valid email address
            if not validate_email(company_email):
                messages.error(request, 'enter valid email address')
                return redirect('sign_in')

            # trying to check if company details that is being registered is exists
            if not (Company.objects.filter(company_name=company_name).exists() and
                    Company.objects.filter(company_email=company_email).exists()):
                if not (User.objects.filter(email=company_email).exists() and
                        User.objects.filter(username=company_name).exists()):
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

                            User.objects.create_user(company_email, password1, username=company_name, is_active=False)
                            user = User.objects.get(username=company_name, email=company_email)
                            # TODO send email address to login user
                            """ Here i can decide to  tell the user to login or send Email for account activation"""
                            current_site = get_current_site(request)
                            mail_subject = 'Activate your account now'
                            message = render_to_string('authentication/account_activate_email.html', {
                                'user': user,
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user)
                            })
                            to_email = user.email
                            email_to_send = EmailMessage(
                                mail_subject,
                                message,
                                to=[to_email]
                            )
                            email_to_send.send()

                            messages.info(self.request, f" activate your account at {company_email[3:]}")
                            return redirect('sign_in')
                        else:
                            messages.info(self.request, "password doesn't match")
                            return redirect('sign_in')

                    else:
                        messages.info(self.request, 'Agree to terms and condition')
                        return redirect('sign_in')
                else:

                    messages.warning(request, 'company name or email address is already taken')
                    return redirect('sign_in')

            else:
                messages.warning(request, 'company name or email address is already taken')
                return redirect('sign_in')

        messages.warning(request, 'Try to fill all information')
        return redirect('sign_in')
