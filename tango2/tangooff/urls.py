from django.urls import path, include
from . import views
        
urlpatterns = [
    path('', views.home, name='tangooff-home'),
    path('practice/<str:level>', views.practice, name='tangooff-practice'),
    path('practice/<str:level>/<str:patch>', views.practice, name='tangooff-practice'),
    path('save/', views.save, name='tangooff-save'),
    path('display/', views.display, name='tangooff-display'),
    path('leaderboard-practice/', views.leaderboardPractice, name='tangooff-leaderboard'),
    # path('test/', views.test, name='tangooff-test'),
    # path('testsave/', views.testsave, name='tangooff-testsave'),
    # path('testdisplay/', views.testdisplay, name='tangooff-testdisplay'),
]