from  django.urls import path
from . import views
# app_name ='core'
urlpatterns = [
<<<<<<< HEAD
path('login',views.signin, name= 'sigin'),
path('homepage/',views.homepage, name= 'homepage'),
=======
# path('',views.signin, name= 'sigin'),
path('',views.homepage, name= 'homepage'),
path('my_profile/',views.my_profile, name= 'my_profile'),
>>>>>>> e00114349fcc8b8ce83c2fd30dd741cd885322e3
path('users_profile/',views.users_profile, name= 'users_profile'),
path('users_profile_details/',views.users_profile_details, name= 'users_profile_details'),

path('companies/',views.companies, name= 'companies'),
path('about_company/',views.about_company, name= 'about_company'),
path('company_profile/',views.company_profile, name= 'company_profile'),

path('jobs/',views.jobs, name= 'jobs'),
path('job_details/',views.job_details, name= 'job_details'),
path('projects/',views. projects, name= 'projects'),
path('project_details/',views.project_details, name= 'project_details'),
path('massages/',views.massages, name= 'massages'),
path('my_profile_account_settings/',views.my_profile_account_settings, name= 'my_profile_account_settings'),
path('forum/',views.forum, name= 'forum'),
path('forum_post_details/',views.forum_post_details, name= 'forum_post_details'),
path('help_center/',views.help_center, name= 'help_center'),
]