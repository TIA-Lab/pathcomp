from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm
from .models import UserCertificate
from xhtml2pdf import pisa 
import os
from tango2.settings import BASE_DIR
from fpdf import FPDF, HTMLMixin

# Create your views here.
def home(request):
    context = {
        'top': 'home'
    }
    return render(request, 'tangoweb/home.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         print(form)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             user = form.save()
#             return redirect('tangoweb-home')
#     else:
#         form = UserRegisterForm()
    
#     return render(request, 'tangoweb/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        userform = UserRegisterForm(request.POST)
        userprofileform = UserProfileForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            username = userform.cleaned_data.get('username')

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            return redirect('tangoweb-home')
    else:
        userform = UserRegisterForm()
        userprofileform = UserProfileForm()
    
    return render(request, 'tangoweb/register.html', {'userform': userform, 'userprofileform': userprofileform})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                if request.POST.get('next') != '':
                    return redirect(request.POST.get('next', 'tangoweb-home'))
                else: 
                    return redirect('tangoweb-home')
            else:
                messages.warning(request, f'Please login with correct username and password')
                return redirect('tangoweb-login')

    return render(request, 'tangoweb/login.html')


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)

def termsandconditions(request):
    context = {
        'top': 'information',
    }
    return render(request, 'tangoweb/termsandconditions.html', context)    


def forteachers(request):
    context = {
        'top': 'information',
    }
    return render(request, 'tangoweb/forteachers.html', context)    


def certificateinformation(request):
    context = {
        'top': 'information',
    }
    return render(request, 'tangoweb/certificateinformation.html', context)    


def contactus(request):
    context = {
        'top': 'contactus',
    }
    return render(request, 'tangoweb/contactus.html', context)    


@login_required
def certificate(request):

    if request.method == 'POST':
        name = request.POST.get('username')

        # Create a certificate and save it to Database.
        aCertificate  = UserCertificate()
        aCertificate.name = name
        aCertificate.user = request.user
        aCertificate.downloadcount = 0
        aCertificate.save()

    certificates = UserCertificate.objects.filter(user=request.user)
    context = {
        'top': 'certificate',
        'certificates': certificates
    }
    return render(request, 'tangoweb/certificate.html', context)  


class HtmlPdf(FPDF, HTMLMixin):
    pass

def certificateprinting(request, id=None):    
    aCertificate = UserCertificate.objects.get(pk=id)
    if aCertificate == None:
        return HttpResponse('<h2>Sorry that there is a problem in certification generation. Please contact an administrator</h2>')

    aCertificate.downloadcount += 1
    aCertificate.save()

    pdf = HtmlPdf()
    pdf.add_page(orientation='L')
    pdf.image(os.path.join(BASE_DIR, 'static/image/certificate.png'), 0, 0, 297, 210)

    print(os.path.join(BASE_DIR, 'static/font/Apple Chancery 100.ttf'))
    pdf.add_font('Apple Chancery 100', '', os.path.join(BASE_DIR, 'static/font/Apple Chancery 100.ttf'), uni=True)
    pdf.set_font('Apple Chancery 100', '', 35)
    
    pdf.ln(h=50)
    pdf.cell(0, 0, aCertificate.name, 0, 1, 'C')   

    
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_pathcomp_certificate.pdf"'
    response['Content-Type'] = 'application/pdf'

    return response


@login_required
def user_logout(request):
    logout(request)
    return redirect('tangoweb-home')


@login_required
def memberlist(request):
    members = User.objects.all()
    print(members)
    context = {
        'top': 'member',
        'members': members
    }
    return render(request, 'tangoweb/memberlist.html', context)    
