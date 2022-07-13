from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from project.models import Category, Institution, Donation, INSTITUTION_TYPE, ExtendUser
from django.core.paginator import Paginator
from django.views.generic import FormView, UpdateView, TemplateView
from project.forms import RegisterForm, ChangePwForm, ResetPwForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.defaulttags import register
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.core.mail import EmailMessage, mail_admins
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.validators import validate_email


def send_activation_email(user, request):
    """ Sends an activation email """
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
    """ Checks if a user clicked on a link sent to him """

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except ObjectDoesNotExist:
        user = None
    if user and generate_token.check_token(user, token):
        user.extenduser.is_user_verified = True
        user.extenduser.save()

        messages.add_message(request, messages.SUCCESS, "Email verified, you can log in now.")
        return redirect(reverse("login"))

    return render(request, 'activation-failed.html', {'user': user})


def contact(request):
    """ Sends a contact email from a user to admin """
    if request.method == "POST":
        message_name = request.POST.get('name')
        message_email = request.POST.get('email')
        message = request.POST.get('message')

        if message_name and message_email and message:
            try:
                validate_email(message_email)
            except ValidationError:
                messages.add_message(request, messages.ERROR, "Email address is incorrect.")
                return render(request, 'index.html')
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
            messages.add_message(request, messages.WARNING, "Fill in all fields, please.")
            return redirect('/')

    else:
        return redirect('/')


# def create(request):
#     if request.method == 'POST':
#         institution_id = request.POST.get('id')
#         donation = Donation.objects.get(id=institution_id)
#         if not donation.is_taken:
#             donation.is_taken = True
#         else:
#             donation.is_taken = False
#         donation.save()
#         success = "DODANO"
#         return HttpResponse(success)
#     else:
#         print("NIE DZIALA")
#         return HttpResponse('CHUJA DZIALA')


class AddDonation(View):
    """ Adds a donation made by a user into a database """
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()

            ctx = {'categories': categories,
                   'institutions': institutions}
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

            messages.add_message(request, messages.ERROR, "Fill in all fields, please.")
            return redirect('login')

        logged_user = authenticate(username=email,
                                   password=pw)
        if logged_user is not None:
            if not logged_user.extenduser.is_user_verified:
                messages.add_message(request, messages.WARNING,
                                     "The account is not verified. Check your email inbox, please.")
                return redirect('login')
            else:
                login(self.request, logged_user)

            return redirect('donation')
        else:
            try:
                User.objects.get(username=email)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR,
                                     "The email and password you entered did not match our records.")
                return redirect('login')
            else:
                messages.add_message(request, messages.ERROR,
                                     "Incorrect password. Enter a valid password to log in, please.")
                return redirect('login')


def send_reset_pw_email(user, email, request):
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


class RemindPassword(View):
    def get(self, request):
        return render(request, 'remind_password.html')
    def post(self, request):
        email = request.POST.get("email")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.add_message(request, messages.ERROR,
                                     "Enter your email address in format 'username@example.com'")
                return redirect('remind_pw')
            else:
                try:
                    user = User.objects.get(username=email)
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.ERROR,
                                         "We couldn't find an account with that email address.")
                    return redirect('remind_pw')
                else:
                    send_reset_pw_email(user, email, request)
                    messages.add_message(request, messages.SUCCESS, "Success! Check your email inbox to continue.")
                    return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "Enter an email address, please.")
            return redirect('remind_pw')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except ObjectDoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        messages.add_message(request, messages.SUCCESS, f'Success {user.first_name}! Enter a new password, please.')
        response = redirect('/new_password/')
        response.set_cookie(key="user_id", value=f"{user.id}")
        return response
    return render(request, 'activation-failed.html')


class SetNewPass(View):
    user_id = ""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('landing_page')
        else:
            form = ResetPwForm()
            response = render(request, 'remind_password_reset.html', {'form': form})
            if request.COOKIES.get('user_id'):
                SetNewPass.user_id = request.COOKIES.get('user_id')
                response.delete_cookie('user_id')
                return response
            else:
                return redirect('landing_page')

    def post(self, request):
        form = ResetPwForm(request.POST)
        if form.is_valid():

            user = User.objects.get(id=SetNewPass.user_id)
            SetNewPass.user_id = ""
            pw1 = form.cleaned_data['new_pw_1']
            user.set_password(pw1)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'The password has been changed.')
            return redirect('login')
        else:
            response = redirect('new_pw')
            response.set_cookie(key='user_id', value=SetNewPass.user_id)
            messages.add_message(request, messages.WARNING,
                                 'The passwords you typed in do not match. Try again, please.')
            return response


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

        new_user = User.objects.create_user(username=email, first_name=name, last_name=surname,
                                            email=email, password=pw)
        extend_user = ExtendUser.objects.create(user=new_user)

        send_activation_email(new_user, self.request)

        messages.add_message(self.request, messages.SUCCESS,
                             'We sent you an email to verify your account.')

        return super().form_valid(form)


class UserProfile(View):
    def get(self, request):
        user_donations = Donation.objects.filter(user=request.user.id)\
                                         .filter(is_taken="False")
        user_donations_archive = Donation.objects.filter(user=request.user.id)\
                                                 .filter(is_taken="True")
        ctx = {"user_donations": user_donations,
               "user_donations_archive": user_donations_archive}
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
            messages.add_message(request, messages.ERROR, "Incorrect password. Enter a valid password, please.")
            return render(request, 'user_profile_edit.html')


class UserChangePw(FormView):
    form_class = ChangePwForm
    template_name = 'change_pw.html'

    def form_valid(self, form):
        old = form.cleaned_data['old_pw']
        new1 = form.cleaned_data['new_pw_1']
        logged_user = User.objects.get(id=self.request.user.id)

        if check_password(old, logged_user.password):
            logged_user.set_password(new1)
            logged_user.save()
            update_session_auth_hash(self.request, logged_user)

            return redirect('profile')
        else:
            messages.add_message(self.request, messages.ERROR, 'Incorrect password. Enter a valid password, please.')
            return redirect(reverse_lazy('change-pw'))


#, sprzęt AGD, ciepłe koce