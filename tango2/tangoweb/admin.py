from django.contrib import admin
from .models import UserPractice, UserCompetition, UserPracticeBoard

# Register your models here.
admin.site.register(UserPractice)
admin.site.register(UserPracticeBoard)
admin.site.register(UserCompetition)
