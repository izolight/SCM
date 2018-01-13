from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    """
    start page
    :param request:  client request
    :return: home screen
    """
    return render(request, 'index.html')


def contact(request):
    """
    Shows App. contacts
    :param request: client request
    :return: page with contact details
    """
    return render(request, 'contact.html')


def impressum(request):
    """
    Shows the impressum page
    :param request: client request
    :return: impressum page
    """
    return render(request, 'impressum.html')


@login_required()
def create_account(request):
    """
    todo: needed for multi tenancy if planned for implementation
    :param request: client request
    :return:
    """
    return render(request, 'create_account.html')