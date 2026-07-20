from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, AddressCreationForm
# from .forms import RegisterForm, CheckOtpForm
import ghasedak_sms
from random import randint
# from .models import Otp, User
from uuid import uuid4
from django.utils.crypto import get_random_string

SMS = ghasedak_sms.Ghasedak("A place where you can put the API Key")


# def user_login(request):
#     return render(request, template_name="account/login.html", context={})


class OtpLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, template_name="account/login.html", context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error("phone", "invalid user data")
        else:
            form.add_error("phone", "invalid data")

        return render(request, template_name="account/login.html", context={"form": form})


# class RegisterView(View):
#     def get(self, request):
#         form = RegisterForm()
#         return render(request, template_name="account/otp_login.html", context={"form": form})
#
#     def post(self, request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             randcode = randint(1000, 9999)
#             SMS.verification(
#                 {"receptor": cd["phone"], 'type': '1', 'template': 'randcode', 'param1': randcode})
#             token = str(uuid4())
#             Otp.objects.crate(phone =cd["phone"], code=randcode, token=token)
#             print(randcode)
#             return redirect(reverse("account:check_otp") + f'?token={token}')
#         else:
#             form.add_error("phone", "invalid data")
#
#         return render(request, template_name="account/otp_login.html", context={"form": form})
#
#
# class CheckOtpView(View):
#     def get(self, request):
#         form = CheckOtpForm()
#         return render(request, template_name="account/check_otp.html", context={"form": form})
#
#     def post(self, request):
#         token = request.GET.get("token")
#         form = CheckOtpForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             if Otp.objects.filter(code=["code"], token=token).exists():
#                 otp = Otp.objects.get(token=token)
#                 user, is_create = User.objects.get_or_create(phone=otp.phone)
#                 login(request, user, backend="django.contrib.auth.backends.ModelBackend")
#                 otp.delete()
#                 return redirect("/")
#         else:
#             form.add_error("phone", "invalid data")
#
#         return render(request, template_name="account/check_otp.html", context={"form": form})


class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

        return render(request, template_name="account/add_address.html", context={"form": form})

    def get(self, request):
        form = AddressCreationForm()
        return render(request, template_name="account/add_address.html", context={"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")