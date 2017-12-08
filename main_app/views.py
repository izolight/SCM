from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse

from django.contrib.auth.decorators import login_required

from main_app.forms import SignUpForm, AddMemberForm, AddIceForm
from main_app.models import City, Member, Invoice, IceSlot, Training


def index(request):
    return render(request, 'index.html')


@login_required()
def ajax_city_from_zip(request, zip):
    cities = get_city_from_zip(zip)


@login_required()
def get_city_from_zip(zip):
    return City.objects.filter(zip_code=zip)


@login_required()
def add_member(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
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
            messages.add_message(request, messages.SUCCESS, f'Added member {user.first_name} {user.last_name}')
            return redirect('list_members')
    else:
        form = AddMemberForm()

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
    return render(request, 'registration/sign_up.html', {
        'form': form
    })


@login_required()
def list_members(request):
    members = Member.objects.all()
    return render(request, 'list_members.html', {
        'members': members
    })


@login_required()
def list_member(request, member_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    # TODO logic for listing single member
    member = Member.objects.get(pk=member_id)
    if not member:
        return HttpResponseNotFound()
    return render(request, 'list_member.html', {
        'member': member
    })


@login_required()
def delete_member(request, member_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    # TODO logic for deleting
    member = Member.objects.get(pk=member_id)
    if not member:
        return HttpResponseNotFound()
    member.delete()
    messages.add_message(request, messages.SUCCESS, f'Deleted member {member_id}')
    return HttpResponse(status=204)


#    return render(request, 'delete_member.html')

@login_required()
def edit_member(request, member_id):
    member = Member.objects.get(pk=member_id)
    if not member:
        return HttpResponseNotFound()
    if request.method == 'POST':
        # TODO logic for editing
        return redirect('list_members')
    return render(request, 'edit_member.html', {
        'member': member
    })

@login_required()
def create_invoice(request):
    return render(request, 'create_invoice.html')


@login_required()
def list_invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'list_invoices.html', {
        'invoices': invoices
    })


@login_required()
def edit_invoice(request, invoice_id):
    return render(request, 'edit_invoice.html')


def contact(request):
    return render(request, 'contact.html')


@login_required()
def list_ices(request):
    ice_slots = IceSlot.objects.all()
    return render(request, 'list_ices.html', {
        'ice_slots': ice_slots
    })


@login_required()
def add_ice(request):
    if request.method == 'POST':
        form = AddIceForm(request.POST)
        if form.is_valid():
            ice_slot = IceSlot(
                date=form.cleaned_data['date'],
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                club=request.user.member.club
            )
            ice_slot.save()
            ice_slot.refresh_from_db()
            messages.add_message(request, messages.SUCCESS,
                                 f'Added ice_slot at {ice_slot.date} {ice_slot.start_time} for club {ice_slot.club.name}')
            return redirect('list_ices')
    else:
        form = AddIceForm()
    return render(request, 'add_ice.html', {
        'form': form
    })

    @login_required()
    def edit_ice(request, ice_slot_id):
        return render(request, 'edit_ice.html')

    @login_required()
    def delete_ice(request, ice_slot_id):
        if request.method != 'POST':
            return HttpResponseBadRequest()
        # TODO logic for deleting
        ice_slot = get_object_or_404(IceSlot, pk=ice_slot_id)
        ice_slot.delete()
        messages.add_message(request, messages.SUCCESS, f'Deleted ice_slot {ice_slot_id}')
        return HttpResponse(status=204)
        # return render(request, 'delete_ice.html')

    def impressum(request):
        return render(request, 'impressum.html')

    @login_required()
    def create_account(request):
        return render(request, 'create_account.html')

    @login_required()
    def list_trainings(request):
        trainings = Training.objects.all()
        return render(request, 'list_trainings.html', {
            'trainings': trainings
        })

    @login_required()
    def view_training(request, training_id):
        return render(request, 'view_training.html')

    @login_required()
    def add_training(request):
        return render(request, 'add_training.html')

    @login_required()
    def edit_training(request, training_id):
        return render(request, 'edit_training.html')

    @login_required()
    def delete_training(request, training_id):
        if request.method != 'POST':
            return HttpResponseBadRequest()
        # TODO logic for deleting
        training = Training.objects.get(pk=training_id)
        if not training:
            return HttpResponseNotFound()
        training.delete()
        messages.add_message(request, messages.SUCCESS, f'Delete training {training_id}')
        return HttpResponse(status=204)
        # return render(request, 'delete_training.html')
