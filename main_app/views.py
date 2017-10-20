from django.shortcuts import render, redirect
from .forms import NewMemberForm
from django.contrib.auth import authenticate, login
from .models import City


# Create your views here.
def index(request):
    return render(request, 'index.html')


def ajax_city_from_zip(request, zip):
    cities = get_city_from_zip(zip)


def get_city_from_zip(zip):
    return City.objects.filter(zip_code=zip)


def add_member(request):
    if request.method == 'POST':
        form = NewMemberForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.member.address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            zip_code = form.cleaned_data.get('zip_code')

#            user.member.city = form.cleaned_data.get('city')
            user.member.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('list_members')
    else:
        form = NewMemberForm()
        return render(request, 'add_member.html', {
            'form': form
        })


def list_members(request):
    return render(request, 'list_member.html')


def member_delete(request):
    return render(request, 'delete_member.html')


def member_edit(request):
    return render(request, 'edit_member.html')


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
