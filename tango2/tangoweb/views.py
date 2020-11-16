from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm
from xhtml2pdf import pisa 
import os
from tango2.settings import BASE_DIR

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

def certificate(request):
    context = {
        'top': 'certificate',
    }
    return render(request, 'tangoweb/certificate.html', context)  

# def certificateprinting(request):
#     data = {
#         'name': 'Young Saeng Park'
#     }

#     template = get_template('tangoweb/certificateformat.html')
#     html  = template.render(data)

#     file = open('test.pdf', "w+b")
#     pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')

#     file.seek(0)
#     pdf = file.read()
#     file.close()            
#     return HttpResponse(pdf, 'application/pdf') 

# def certificateprinting(request):
#     from fpdf import FPDF
#     pdf = FPDF(format='letter')
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="Welcome to Python!", align="C")
#     pdf.output("Somefilename.pdf", 'I')
    
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = "attachment; filename=Somefilename.pdf"

#     return response

from fpdf import FPDF, HTMLMixin

class HtmlPdf(FPDF, HTMLMixin):
    pass

def certificateprinting(request):    
    pdf = HtmlPdf()
    # pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
    pdf.add_page(orientation='L')
    pdf.image(os.path.join(BASE_DIR, 'static/image/certificate.png'), 0, 0, 297, 210)

    name = ''
    print(request.method)
    if request.method == 'POST':
        name = request.POST.get('username')
        print(request.POST)
        print(name)

    # pdf.add_font('Hello Valentina', '', os.path.join(BASE_DIR, 'static/font/Hello Valentina.ttf'), uni=True)
    # pdf.set_font('Hello Valentina', '', 40)
    
    pdf.add_font('Apple Chancery 100', '', os.path.join(BASE_DIR, 'static/font/Apple Chancery 100.ttf'), uni=True)
    pdf.set_font('Apple Chancery 100', '', 35)
    
    pdf.ln(h=60)
    pdf.cell(0, 0, name, 0, 1, 'C')   
    # data = {
    #     'name': name
    # }
    # template = get_template('tangoweb/certificateformat.html')
    # html  = template.render(data)
    # pdf.write_html(html)
    

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
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
