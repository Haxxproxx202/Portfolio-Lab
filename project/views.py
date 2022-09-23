from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from project.models import Category, Institution, Donation, INSTITUTION_TYPE, ExtendUser
from django.views.generic import FormView
from project.forms import RegisterForm, ChangePwForm, ResetPwForm, LoginForm, RemindPasswordForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage, mail_admins
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.validators import validate_email
from django.contrib.auth.mixins import LoginRequiredMixin


class LandingPage(View):
    """ Shows the main page. """
    def get(self, request):

        donations = Donation.objects.all()
        sacks_qty = 0
        for i in donations:
            sacks_qty += i.quantity

        foundations_qty = Institution.objects.count()
        all_foundations = Institution.objects.filter(type="1")
        all_non_govt = Institution.objects.filter(type="2")
        all_local = Institution.objects.filter(type="3")

        foundations_1_2 = all_foundations[:2]
        foundations_3_4 = all_foundations[2:4]
        non_govt_1_2 = all_non_govt[:2]
        non_govt_3_4 = all_non_govt[2:4]
        non_govt_5_6 = all_non_govt[4:6]
        non_govt_7_8 = all_non_govt[6:8]
        local_1_2 = all_local[:2]
        local_3_4 = all_local[2:4]

        # Pagination Django (refreshes the site)
        # p = Paginator(all_foundations, 2)
        # page = request.GET.get('page')
        # pagina = p.get_page(page)

        ctx = {'sacks_qty': sacks_qty,
               'inst_qty': foundations_qty,
               'foundations_1_2': foundations_1_2,
               'foundations_3_4': foundations_3_4,
               'non_govt_1_2': non_govt_1_2,
               'non_govt_3_4': non_govt_3_4,
               'non_govt_5_6': non_govt_5_6,
               'non_govt_7_8': non_govt_7_8,
               'local_1_2': local_1_2,
               'local_3_4': local_3_4}
        return render(request, 'index.html', ctx)


class Login(FormView):
    """ Lets user log in. """
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/form/'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']

        logged_user = authenticate(username=email, password=password)

        if logged_user is not None:
            if not logged_user.extenduser.is_user_verified:
                messages.add_message(self.request, messages.WARNING,
                                     "The account is not verified. Check your email inbox, please.")
                return redirect('login')
            else:
                login(self.request, logged_user)
                return super().form_valid(form)
        else:
            try:
                User.objects.get(username=email)
            except ObjectDoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     "User with that email address does not exist.")
                return redirect('login')
            else:
                messages.add_message(self.request, messages.ERROR,
                                     "Incorrect password. Enter a valid password to log in, please.")
                return redirect('login')


class Logout(View):
    """ Logs user out. """
    def get(self, request):
        logout(request)
        return redirect('/')


class Register(FormView):
    """ Registers a new user and calls a 'send_activation_email' function to activate the user's account . """
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        name = form.cleaned_data['first_name']
        surname = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        pw = form.cleaned_data['pass1']

        new_user = User.objects.create_user(username=email, first_name=name, last_name=surname,
                                            email=email, password=pw)
        ExtendUser.objects.create(user=new_user)
        send_activation_email(new_user, self.request)

        messages.add_message(self.request, messages.SUCCESS,
                             'We sent you an email to verify your account.')

        return super().form_valid(form)


def send_activation_email(user, request):
    """ Sends an activation email. """
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string('emails/account_activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject,
                         body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email])
    email.send()


def activate_user(request, uidb64, token):
    """ The function is called when a user clicks on an account activation link sent to him via email. """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except ObjectDoesNotExist:
        user = None
    if user and generate_token.check_token(user, token):
        user.extenduser.is_user_verified = True
        user.extenduser.save()
        messages.add_message(request, messages.SUCCESS, "Email verified successfully. You can log in now.")

        return redirect(reverse("login"))
    return render(request, 'activation-failed.html', {'user': user})


class RemindPassword(FormView):
    """ Calls a 'send_reset_pw_email' function if email is valid. """
    form_class = RemindPasswordForm
    template_name = 'remind_password.html'
    success_url = '/login/'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        try:
            validate_email(email)
        except ValidationError:
            messages.add_message(self.request, messages.ERROR, "The email must be in format: my_email@example.com")
            return redirect('remind_pw')
        else:
            try:
                user = User.objects.get(username=email)
            except ObjectDoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     "We couldn't find an account with that email address.")
                return redirect('remind_pw')
            else:
                send_reset_pw_email(self.request, user, email)
                messages.add_message(self.request, messages.SUCCESS, "Success! Check your email inbox to continue.")
                return super().form_valid(form)


def send_reset_pw_email(request, user, email):
    """ Sends user an email with a single-use link in order to set a new password. """
    email_subject = "Password reset"
    email_body = render_to_string('emails/remind_password_email.html',
                                  {'user_name': user.first_name,
                                   'domain': get_current_site(request),
                                   'uid': urlsafe_base64_encode(force_bytes(user.id)),
                                   'token': default_token_generator.make_token(user),
                                   'protocol': 'http'})

    verification_email = EmailMessage(subject=email_subject,
                                      body=email_body,
                                      from_email=settings.EMAIL_FROM_USER,
                                      to=[email])
    verification_email.send()


def password_reset_confirm(request, uidb64, token):
    """ The function is called when a user clicks on a password reset link sent to him via email. """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except ObjectDoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        messages.add_message(request, messages.SUCCESS, f'Success {user.first_name}! Enter a new password, please.')
        response = redirect('/new_password/')
        # response.set_cookie(key="user_id", value=f"{user.id}")
        SetNewPass.user_id = user.id
        return response
    return render(request, 'activation-failed.html')


class SetNewPass(View):
    """ Sets a new password after email confirmation. """
    user_id = ""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('landing_page')
        else:
            form = ResetPwForm()
            response = render(request, 'remind_password_reset.html', {'form': form})
            # if request.COOKIES.get('user_id'):
            #     SetNewPass.user_id = request.COOKIES.get('user_id')
            #     response.delete_cookie('user_id')
            #     return response
            # else:
            #     return redirect('landing_page')
            return response

    def post(self, request):
        form = ResetPwForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(id=SetNewPass.user_id)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, 'Something went wrong. Try again, please.')
                return redirect('remind_pw')
            else:
                SetNewPass.user_id = ""
                pw1 = form.cleaned_data['new_pw_1']
                user.set_password(pw1)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'The password has been changed.')
                return redirect('login')
        else:
            response = redirect('new_pw')
            # response.set_cookie(key='user_id', value=SetNewPass.user_id)
            messages.add_message(request, messages.WARNING,
                                 'Password must contain at least 1 uppercase letter, 1 digit and they both must match.')
            return response


class AddDonation(View):
    """ Adds a donation record made by a user into a database. """
    def get(self, request):
        if request.user.is_authenticated:
            ctx = {'categories': Category.objects.all(),
                   'institutions': Institution.objects.all()}
            return render(request, 'form.html', ctx)
        else:
            messages.add_message(request, messages.INFO, "To make a donation you have to log in first.")
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

        if number_of_bags != "" and organization and address != "" and city != "" \
                and postcode != "" and phone != "" and date != "" and time != "" and cats_list:

            full_address = address + ", " + city
            donation = Donation.objects.create(quantity=number_of_bags,
                                               institution=Institution.objects.get(id=organization),
                                               address=full_address,
                                               phone_number=phone,
                                               zip_code=postcode,
                                               pick_up_date=date,
                                               pick_up_time=time,
                                               pick_up_comment=more_info,
                                               user=User.objects.get(id=request.user.id))
            for i in cats_list:
                cat = Category.objects.get(id=i)
                donation.categories.add(cat)

            return render(request, 'form-confirmation.html')
        else:
            messages.add_message(request, messages.ERROR, "To make a donation you have to fill in every field.")

            return redirect('/form/')


class FormConfirmation(LoginRequiredMixin, View):
    """ Shows a confirmation template. """
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfile(LoginRequiredMixin, View):
    """ Shows a user's profile. """
    def get(self, request):
        user_donations = Donation.objects.filter(user=request.user.id)\
                                         .filter(is_taken="False")
        user_donations_archive = Donation.objects.filter(user=request.user.id)\
                                                 .filter(is_taken="True")
        ctx = {"user_donations": user_donations,
               "user_donations_archive": user_donations_archive}
        return render(request, 'user_profile.html', ctx)


def donation_archiving(request):
    """ In cooperation with AJAX, saves information without page refreshing about donation archiving into a database """
    if request.method == 'POST':
        institution_id = request.POST.get('id')
        donation = Donation.objects.get(id=institution_id)
        if not donation.is_taken:
            donation.is_taken = True
        else:
            donation.is_taken = False
        donation.save()
        return HttpResponse()
    else:
        return HttpResponse()


class UserSettings(LoginRequiredMixin, View):
    """ Allows to change a user's personal data. """
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
            messages.add_message(request, messages.ERROR, "Incorrect password. Enter a valid password, please.")
            return render(request, 'user_profile_edit.html')


class UserChangePw(LoginRequiredMixin, FormView):
    """ Allows a logged-in user to change a password to an account. """
    form_class = ChangePwForm
    template_name = 'change_pw.html'

    def form_valid(self, form):
        current_pw = form.cleaned_data['current_pw']
        new_pw = form.cleaned_data['new_pw_1']
        logged_user = User.objects.get(id=self.request.user.id)

        if check_password(current_pw, logged_user.password):
            logged_user.set_password(new_pw)
            logged_user.save()
            update_session_auth_hash(self.request, logged_user)
            return redirect('profile')
        else:
            messages.add_message(self.request, messages.ERROR, 'Incorrect password. Enter a valid password, please.')
            # return redirect(reverse_lazy('change-pw'))
            return render(self.request, 'change_pw.html', {'form': form})


def user_contact(request):
    """ Sends a contact email from user to admin. """
    if request.method == "POST":
        message_name = request.POST.get('name')
        message_email = request.POST.get('email')
        message = request.POST.get('message')

        if message_name and message_email and message:
            try:
                validate_email(message_email)
            except ValidationError:
                messages.add_message(request, messages.ERROR, "Email address is incorrect.")
                return redirect('/')
            else:
                message_edited = f"""
                Email sent by: {message_name}
                Sender's email address: {message_email}

                Content:
                {message}
                """

                mail_admins(message_name,
                            message_edited,
                            fail_silently=False
                            )
                return render(request, 'index.html', {'message_name': message_name})
        else:
            messages.add_message(request, messages.WARNING, "To send us a message fill in all the fields, please.")
            return redirect('/')
    else:
        return redirect('/')
