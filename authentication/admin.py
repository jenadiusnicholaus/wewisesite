from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProfessionalType)
admin.site.register(UserAddress)
admin.site.register(UserSuggestions)
admin.site.register(UserEducation)
admin.site.register(UserExperiences)
admin.site.register(UserSkills)
admin.site.register(UserPortfolio)
admin.site.register(Follow)




