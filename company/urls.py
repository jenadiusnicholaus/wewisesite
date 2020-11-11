from django.urls import path
from . import views

urlpatterns = [
    path('comp_signup/',views.CompanySignUp.as_view(), name='comp_signup')
]
