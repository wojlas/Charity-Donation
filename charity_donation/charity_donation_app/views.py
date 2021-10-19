from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/index.html')

class DonationView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/form.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/login.html')