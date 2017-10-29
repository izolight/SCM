from main_app.forms import NewMemberForm, SignUpForm
from main_app.models import City
from django.shortcuts import render, redirect
from .forms import NewMemberForm
from django.contrib.auth.models import User
from .models import City, Member
from django.contrib.auth import authenticate, login


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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('loggedInLandingPage')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def list_members(request):
    members = Member.objects.all()
    return render(request, 'list_members.html', {
        'members': members
    })


def delete_member(request):
    return render(request, 'delete_member.html')


def edit_member(request):
    return render(request, 'edit_member.html')


def list_bills(request):
    return render(request, 'list_bills.html')


def open_bill(request):
    return render(request, 'open_bill.html')


def facturate_bill(request):
    return render(request, 'facturate_bill.html')


def facturated_bill(request):
    return render(request, 'facturated_bill.html')


def delayed_bill(request):
    return render(request, 'delayed_bill.html')


def reminded_bill(request):
    return render(request, 'reminded_bill.html')


def register_bill(request):
    return render(request, 'payed_bill.html')


def notpayed_bill(request):
    return render(request, 'notpayed_bill.html')


def contact(request):
    return render(request, 'contact.html')


def plan_ice(request):
    return render(request, 'plan_ice.html')


def list_ices(request):
    return render(request, 'list_ices.html')


def add_ice(request):
    return render(request, 'add_ice.html')


def edit_ice(request):
    return render(request, 'edit_ice.html')


def delete_ice(request):
    return render(request, 'delete_ice.html')


def impressum(request):
    return render(request, 'impressum.html')


def create_account(request):
    return render(request, 'create_account.html')


def list_trainings(request):
    return render(request, 'list_trainings.html')


def add_training(request):
    return render(request, 'add_training.html')


def edit_training(request):
    return render(request, 'edit_training.html')


def delete_training(request):
    return render(request, 'delete_training.html')
