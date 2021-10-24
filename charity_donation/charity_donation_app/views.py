from accounts.models import CustomUser
from django.shortcuts import render, redirect
from django.views import View

from charity_donation_app.models import Donation, Institution


class IndexView(View):
    def get(self, request):
        ctx = {'bags': Donation.objects.count(),
               'institutions': Institution.objects.count(),
               'fundations': Institution.objects.filter(type='fundation'),
               'no_gov': Institution.objects.filter(type='NGO'),
               'locally': Institution.objects.filter(type='localy'),
               }
        return render(request, 'charity_donation_app/index.html', ctx)


class DonationView(View):
    def get(self, request):
        return render(request, 'charity_donation_app/form.html')


class RegisterView(View):
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
    def get(self, request):
        return render(request, 'charity_donation_app/login.html')
