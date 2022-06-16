from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from project.models import Category, Institution, Donation, INSTITUTION_TYPE
from django.core.paginator import Paginator
from django.views.generic import FormView, UpdateView
from project.forms import RegisterForm, ChangePwForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.messages import constants as messages
from django.template.defaulttags import register
from django.contrib.auth.hashers import check_password


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

    def post(self, request):
        number_of_bags = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('data')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')

        cats_list = request.POST.getlist('categories')

        if cats_list and number_of_bags != "" and organization and address != "" \
                and city != "" and postcode != "" and isinstance(postcode, int) \
                and phone != "" and isinstance(phone, int) and date != "" and time != "":

            full_address = address + ", " + city
            org = Institution.objects.get(id=organization)
            user = User.objects.get(id=request.user.id)

            donation = Donation.objects.create(quantity=number_of_bags,
                                               institution=org,
                                               address=full_address,
                                               phone_number=phone,
                                               zip_code=postcode,
                                               pick_up_date=date,
                                               pick_up_time=time,
                                               pick_up_comment=more_info,
                                               user=user)
            for i in cats_list:
                cat = Category.objects.get(id=i)
                donation.categories.add(cat)

            return render(request, 'form-confirmation.html')
        else:
            categories = Category.objects.all()
            institutions = Institution.objects.all()

            ctx = {'categories': categories,
                   'institutions': institutions,
                   'error': 'Fill in the entire form correctly, please.'}
            return render(request, 'form.html', ctx)


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

class UserProfil(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_donations = Donation.objects.filter(user=request.user.id)
        ctx = {"user_donations": user_donations}

        return render(request, 'user_profile.html', ctx)

class UserSettings(View):
    def get(self, request):
        
        return render(request, 'user_profile_edit.html')
    def post(self, request):

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('pass')
        if check_password(password, request.user.password):

            user = User.objects.get(id=request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('profile')

        else:
            error = "Type in a correct password"
            return render(request, 'user_profile_edit.html', {'error': error})

class UserChangePw(FormView):
    form_class = ChangePwForm
    template_name = 'change_pw.html'

    def form_valid(self, form):
        old = form.cleaned_data['old_pw']
        new1 = form.cleaned_data['new_pw_1']
        user = User.objects.get(id=self.request.user.id)

        if check_password(old, user.password):
            user.set_password(new1)
            user.save()
            update_session_auth_hash(self.request, user)

            return redirect('profile')
        else:
            return reverse_lazy('change-pw')













#, sprzęt AGD, ciepłe koce