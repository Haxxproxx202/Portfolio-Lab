from django.shortcuts import render, redirect
from django.views import View
from project.models import Category, Institution, Donation, INSTITUTION_TYPE
from django.core.paginator import Paginator
from django.views.generic import FormView
from project.forms import RegisterForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.messages import constants as messages
from django.template.defaulttags import register


@register.filter
def get_value(value):
    return value[1]

class AddDonation(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()

            ctx = {'categories': categories,
                   'institutions': institutions}
            return render(request, 'form.html', ctx)
        else:
            return redirect('login')

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
    def post(self, request):
        email = request.POST.get('email')
        pw = request.POST.get('password')

        if not email or not pw:

            error = "Fill in all fields"
            return render(request, 'login.html', {'error': error})

        logged_user = authenticate(username=email,
                                   password=pw)

        if logged_user is not None:
            login(self.request, logged_user)
            return redirect('donation')
        else:
            errot = ''
            return redirect('register')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        name = form.cleaned_data['first_name']
        surname = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        pw = form.cleaned_data['pass2']

        new_user = User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=pw)



        return super().form_valid(form)



#, sprzęt AGD, ciepłe koce