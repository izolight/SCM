from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def member_add(request):
    return render(request, 'member_add.html')


def member_directory(request):
    return render(request, 'member_directory.html')


def member_delete(request):
    return render(request, 'member_delete.html')


def member_edit(request):
    return render(request, 'member_edit.html')


def billing(request):
    return render(request, 'billing.html')


def contact(request):
    return render(request, 'contact.html')


def ice_management(request):
    return render(request, 'ice_management.html')


def impressum(request):
    return render(request, 'impressum.html')


def login(request):
    return render(request, 'login.html')


def material(request):
    return render(request, 'material.html')


def trainings(request):
    return render(request, 'trainings.html')
