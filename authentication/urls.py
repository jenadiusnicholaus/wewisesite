from django.urls import path

from . import views
# app_name ='authentication'
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('my_profile/',views.my_profile, name= 'my_profile'),
    path('signed_up/', views.UserSignUp.as_view(), name='sign_up'),
    path('sign_in/', views.UserSignIn.as_view(), name='sign_in'),
    path('signed_out/', views.user_sign_out, name='sign_out'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profiles', views.ProfilesListView.as_view(), name='profiles'),
    path('following/<int:pk>', views.following, name='following'),
    path('testing/', views.testing, name='testing'),

    # password reset
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    # password reset request
    path("password_reset/", views.password_reset_request, name="password_reset")
]



