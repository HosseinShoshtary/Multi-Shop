from django.shortcuts import render


def user_login(request):
    return render(request, template_name="account/contact.html", context={})