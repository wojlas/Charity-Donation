from django.contrib.auth.models import User
from django.shortcuts import render

from django.views import View

from charity_donation_app.models import Donation, Institution




class IndexView(View):
    def get(self, request):
        ctx = {'bags': Donation.objects.count(),
               'institutions': Institution.objects.count()}
        return render(request, 'charity_donation_app/index.html', ctx)

class DonationView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/form.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/login.html')