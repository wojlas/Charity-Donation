import json, urllib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import CustomUser
from charity_donation_app.models import Donation, Institution, Category


class IndexView(View):
    """App landing page

    Informations about organizations, how it work, statistics and more"""

    def get(self, request):
        ctx = {'bags': Donation.objects.all().annotate(Count('quantity', distinct=True)),
               'institutions': Donation.objects.all().annotate(Count('institution', distinct=True)),
               'fundations': Institution.objects.filter(type='fundation'),
               'no_gov': Institution.objects.filter(type='NGO'),
               'locally': Institution.objects.filter(type='localy'),
               }
        return render(request, 'charity_donation_app/index.html', ctx)


class DonationView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        ctx = {'categories': Category.objects.all(),
               'institutions': Institution.objects.all().prefetch_related("categories")}
        return render(request, 'charity_donation_app/form.html', ctx)

    def post(self, request):
        json_data = json.loads(request.POST)
        bags = json_data['quantity']
        address = json_data['address']
        city = json_data['city']
        postcode = json_data['zip_code']
        phone = json_data['phone_number']
        data = json_data['data']
        time = json_data['time']
        info = json_data['pick_up_coment']
        categories = json_data['categories']
        receiver = json_data['receiver']
        print(address)
        return render(request, 'charity_donation_app/form-confirmation.html')


class RegisterView(View):
    "Register new user"

    def get(self, request):
        return render(request, 'charity_donation_app/register.html')

    def post(self, request):
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("password2")
        if pass1 == pass2:
            CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=pass1)
            return redirect('/login/')
        else:
            return render(request, 'charity_donation_app/register.html')


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

class UserProfileView(View):
    """Profile page"""
    def get(self, request):
        ctx = {'donations': Donation.objects.filter(user=request.user).order_by('-pick_up_date', '-pick_up_time')}
        return render(request, 'charity_donation_app/profile.html', ctx)
