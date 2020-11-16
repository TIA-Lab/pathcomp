from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserPractice(models.Model):
    patch = models.CharField(max_length=100)
    questioncount = models.IntegerField()
    answercount = models.IntegerField()
    correctcount = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.patch
    

class UserPracticeBoard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField()
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} : {self.point}'


class UserCompetition(models.Model):
    patch = models.CharField(max_length=100)
    level = models.CharField(max_length=10)
    attempt = models.IntegerField(blank=True, null=True)
    questioncount = models.IntegerField()
    answercount = models.IntegerField()
    correctcount = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.patch


class UserCompetitionBoard(models.Model):
    questioncount = models.IntegerField(blank=True, null=True)
    answercount = models.IntegerField(blank=True, null=True)
    correctcount = models.IntegerField(blank=True, null=True)
    level = models.IntegerField()
    attempt = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_stage = models.CharField(max_length=50, null=True)


class UserCertificate(models.Model):
    name = models.CharField(max_length=100)
    downloadcount = models.IntegerField(default=0, null=True)
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)