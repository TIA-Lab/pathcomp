from django.urls import path, include
from . import views
        
urlpatterns = [
    path('', views.home, name='tangoweb-home'),
    path('register/', views.register, name='tangoweb-register'),
    path('login/', views.user_login, name='tangoweb-login'),
    path('logout/', views.user_logout, name='tangoweb-logout'),
    path('member/', views.memberlist, name='tangoweb-member'),
    path('termsandconditions/', views.termsandconditions, name='tangoweb-termsandconditions'),
    path('forteachers/', views.forteachers, name='tangoweb-forteachers'),
    path('contactus/', views.contactus, name='tangoweb-contactus'),
    path('certificate/', views.certificate, name='tangoweb-certificate'),
    path('certificateprinting/', views.certificateprinting, name='tangoweb-certificateprinting'),
    path('certificateinformation/', views.certificateinformation, name='tangoweb-certificateinformation'),
]