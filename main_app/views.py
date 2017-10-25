from django.shortcuts import render, redirect
from .forms import NewMemberForm
from django.contrib.auth.models import User
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
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            phone_number = form.cleaned_data['phone_number']

            user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password)
            user.save()
            user.refresh_from_db()
            user.member.address = address
#            user.member.city = city
            user.member.zip_code = zip_code
            user.member.phone_number = phone_number

            user.save()
            return redirect('list_members')
    else:
        form = NewMemberForm()

    return render(request, 'add_member.html', {
            'form': form
        })


def list_members(request):
    return render(request, 'list_member.html')


def delete_member(request):
    return render(request, 'delete_member.html')


def edit_member(request):
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
