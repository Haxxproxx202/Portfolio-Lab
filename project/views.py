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

        ctx = {'sacks_qty': sacks_qty, 'inst_qty': inst_qty}

        return render(request, 'index.html', ctx)

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')