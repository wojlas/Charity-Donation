from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustomUser
from django.shortcuts import render, redirect
from django.views import View

from charity_donation_app.models import Donation, Institution, Category


class IndexView(View):
    """App landing page

    Informations about organizations, how it work, statistics and more"""
    def get(self, request):
        ctx = {'bags': Donation.objects.count(),
               'institutions': Institution.objects.count(),
               'fundations': Institution.objects.filter(type='fundation'),
               'no_gov': Institution.objects.filter(type='NGO'),
               'locally': Institution.objects.filter(type='localy'),
               }
        return render(request, 'charity_donation_app/index.html', ctx)


class DonationView(LoginRequiredMixin ,View):
    login_url = '/login/'

    def get(self, request):
        ctx = {'categories': Category.objects.all()}
        return render(request, 'charity_donation_app/form.html', ctx)


class RegisterView(View):
    "Register new user"
    def get(self, request):
        return render(request, 'charity_donation_app/register.html')

    def post(self, request):
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        # if pass1 == pass2:
        CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=pass1)
        return redirect('/login/')
        # else:
        #     return render(request, 'charity_donation_app/register.html')


class LoginView(View):
    "Login user using email as login"
    def get(self, request):
        return render(request, 'charity_donation_app/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if CustomUser.objects.filter(email=email):
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'charity_donation_app/login.html')
        else:
            return redirect('/register/')

class LogoutView(View):
    """ Logout user"""
    def get(self, request):
        logout(request)
        return redirect('/')