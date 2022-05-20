from django.shortcuts import render
from django.views import View
from project.models import Category, Institution, Donation

# Create your views here.

class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')

class FormConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')

class LandingPage(View):
    def get(self, request):

        donations = Donation.objects.all()
        sacks_qty = 0
        for i in donations:
            sacks_qty += i.quantity

        inst_qty = Institution.objects.count()
        all_fndn = Institution.objects.filter(type="1")
        all_non_govt = Institution.objects.filter(type="2")

        ctx = {'sacks_qty': sacks_qty,
               'inst_qty': inst_qty,
               'all_fndn': all_fndn,
               'all_non_govt': all_non_govt}

        return render(request, 'index.html', ctx)

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

# ubrania, jedzenie, sprzęt AGD, meble, zabawki, ubrania, meble, zabawki, ubrania, jedzenie, ciepłe koce