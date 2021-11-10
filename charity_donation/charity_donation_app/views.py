import json, urllib
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.models import CustomUser
from charity_donation_app.models import Donation, Institution, Category


class IndexView(View):
    """App landing page

    Informations about organizations, how it work, statistics and more"""

    def get(self, request):
        bags = Donation.objects.aggregate(Sum('categories'))
        ctx = {'bags': bags['categories__sum'],
               'institutions': Donation.objects.values('institution').distinct(),
               'fundations': Institution.objects.filter(type='fundation'),
               'no_gov': Institution.objects.filter(type='NGO'),
               'locally': Institution.objects.filter(type='localy'),
               }
        return render(request, 'charity_donation_app/index.html', ctx)

@method_decorator(csrf_exempt, name='dispatch')
class DonationView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        ctx = {'categories': Category.objects.all(),
               'institutions': Institution.objects.all().prefetch_related("categories")}
        return render(request, 'charity_donation_app/form.html', ctx)

    def post(self, request):

        json_data = json.loads(request.body.decode('utf-8'))
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
        print(categories)
        institution = Institution.objects.get(name=receiver)

        new_donation = Donation.objects.create(quantity=int(bags), institution=institution, adress=address,
                                phone_number=int(phone), zip_code=postcode, pick_up_comment=info, pick_up_time=datetime.strptime(time, '%H:%M').time(),
                                pick_up_date=datetime.strptime(data, '%Y-%m-%d').date() ,city=city, user=request.user)

        for category in categories:
            cat1 = Category.objects.get(pk =int(category))
            new_donation.categories.add(cat1)
        new_donation.save()
        success_response = {'form': 'form-confirmation.html',
                            'url': '/donation/success/'}
        # return redirect('/donation/success')
        return JsonResponse(success_response)

class DonationDoneView(View):
    def get(self, request):
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

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
    """Profile page"""
    def get(self, request):
        ctx = {'donations': Donation.objects.filter(user=request.user).order_by('is_taken', 'pick_up_date', 'pick_up_time')}
        return render(request, 'charity_donation_app/profile.html', ctx)

    def post(self, request):
        json_data = json.loads(request.body.decode('utf-8'))
        institution_id = json_data['institution_id']
        is_active = json_data['is_active']
        active = ''.join(e for e in is_active if e.isalnum()) #is_active == True
        donation = Donation.objects.get(pk=int(institution_id))
        donation.is_taken = active
        donation.save()
        return JsonResponse({'data': 'redirect'})

class UserSettingsView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'charity_donation_app/settings.html')

    def post(self, request):
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('first-name')
        lastname = request.POST.get('last-name')

        user = request.user

        if user.check_password(password):
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            cxt = {'error': 'Zapisano'}
            return render(request, 'charity_donation_app/settings.html', cxt)
        else:
            cxt = {'error': 'Niepoprawne hasło'}
            return render(request, 'charity_donation_app/settings.html', cxt)

class PasswordView(View):
    def post(self, request):
        user = request.user
        old_pas = request.POST.get('old-password')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if user.check_password(old_pas):
            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                ctx = {'passalert': 'Hasło zmienione'}
                return redirect('/profile/settings/', ctx)
            else:
                ctx = {'passalert': 'Pola 2 i 3 muszą być identyczne'}
                return redirect('/profile/settings/', ctx)
        else:
            ctx = {'passalert': 'Złe hasło'}
            return redirect('/profile/settings/', ctx)

