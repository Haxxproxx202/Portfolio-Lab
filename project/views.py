from django.shortcuts import render
from django.views import View
from project.models import Category, Institution, Donation
from django.core.paginator import Paginator
from django.views.generic import FormView
from project.forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

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
        all_local = Institution.objects.filter(type="3")

        pag_fndn = Paginator(all_fndn, 2)
        page = request.GET.get('page')
        pagina = pag_fndn.get_page(page)



        ctx = {'sacks_qty': sacks_qty,
               'inst_qty': inst_qty,
               'all_fndn': all_fndn,
               'all_non_govt': all_non_govt,
               'all_local': all_local,
               'pagina': pagina}

        return render(request, 'index.html', ctx)

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        name = form.cleaned_data['first_name']
        surname = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        pw = form.cleaned_data['pass2']

        new_user = User.objects.create_user(username=username, first_name=name, last_name=surname, email=email, password=pw)

        login(self.request, new_user)

        return super().form_valid(form)


#, sprzęt AGD, ciepłe koce