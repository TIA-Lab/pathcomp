from django.urls import path, include
from . import views
        
urlpatterns = [
    path('', views.home, name='tangoon-home'),
    path('save/<str:level>/<int:attempt>', views.save, name='tangoon-save'),
    path('start/<str:level>', views.start, name='tangoon-start'),
    path('competition/<str:level>/<int:attempt>', views.competition, name='tangoon-competition'),
    path('end/<str:level>/<int:attempt>', views.end, name='tangoon-end'),
    path('leaderboard-competition/<str:level>', views.leaderboardCompetition, name='tangoon-leaderboard')
]