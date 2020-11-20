from datetime import timedelta

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib import messages
from .models import (User, UserProfile, Follow)
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from company.forms import CompanyForm
from validate_email import validate_email


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend)
        # return redirect('home')
        messages.success(request, 'Welcome to wewize.com, login now')
        return redirect('sign_in')
    else:
        return HttpResponse('Activation link is invalid!')


class UserSignUp(View):
    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            profession = form.cleaned_data.get('profession')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('repeat_password')
            # terms agreements
            # try to check if the password match
            # if password != password2:
            #     messages.warning(self.request, f'your Password doesnt match')
            #     return redirect('sign_in')
            if not validate_email(email):
                messages.info(self.request, 'Enter valid email')
                return redirect('sign_in')
            # try to check if the user does exit()
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                # if password == password2:
                User.objects.create_user(email, password, username=username, profession=profession, is_active=False)
                user = User.objects.get(username=username, email=email)
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
                messages.warning(self.request, f'activate your account at ****{email[3:]}')

                return redirect('sign_in')
            else:
                messages.warning(self.request, 'Looks like a username with that email or password already exists')
                return redirect("sign_in")
        else:
            print('from not valid')
            messages.warning(self.request, 'Form not valid')
        return redirect('sign_in')


class UserSignIn(View):
    def get(self, request, *args, **kwargs):
        company_form = CompanyForm()
        context = {
            'form': company_form
        }
        return render(request, template_name='authentication/signin.html', context=context)

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user_auth = authenticate(email=email, password=password)
            if not validate_email(email):
                messages.info(self.request, 'Enter valid email')
                return redirect('sign_in')
            elif user_auth:
                # we need to check if the auth_user is activate to our system
                if user_auth.is_active:
                    # if not request.POST.get('remember_me', None):
                    # make the session to end in one mouth
                    request.session.set_expiry(30.4368)
                    login(request, user_auth)
                    messages.info(self.request, 'welcome home ')
                    return redirect('/')

                else:
                    messages.info(self.request, 'Your account was inactive.Try to activate your account now')
                    return redirect('sign_in')
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(email, password))
                messages.warning(self.request, 'Invalid login details given,')
                return redirect("sign_in")


def user_sign_out(request, ):
    # Log out the user.
    logout(request)
    # Return to homepage.
    messages.warning(request, 'Your signed Out, Login again')
    return redirect('sign_in')


class ProfilesListView(ListView):
    model = User
    template_name = 'authentication/user_profiles.html'
    ordering = ['-created_on']


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = "authentication/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'wewise',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'wewise.com', [user.email], fail_silently=False)

                    except BadHeaderError:
                        return HttpResponse('Invalid header found .')
                    # messages.info(request, f'Email sent to ..... {data[3:]}  ')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
                messages.info(request, 'form not valid')
                print(password_reset_form)
                return render(request=request, template_name="authentication/password_reset.html",
                              context={"password_reset_form": password_reset_form})
    password_reset_form = PasswordResetForm()
    messages.info(request, '  Enter email address to reset your password now')

    return render(request=request, template_name="authentication/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def my_profile(request):
    return render(request, template_name='authentication/profile.html')


def following(request, pk):
    try:
        following = get_object_or_404(User, pk=pk)
    except ObjectDoesNotExist as e:
        raise e
    else:
        relationShip, created = Follow.objects.get_or_create(user_id=request.user, follower=following)
        return redirect('homepage')


def testing(request):
    return render(request, template_name='testing_page.html')
