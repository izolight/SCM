"""
views.py: prepares all views to present (handover) to html render engine by linking to correct template.
"""
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse

from django.contrib.auth.decorators import login_required

from main_app.forms import SignUpForm, AddMemberForm, AddIceForm, CreateInvoiceForm, AddTrainingForm
from main_app.models import City, Member, Invoice, IceSlot, Training


def index(request):
    """
    start page
    :param request:  client request
    :return: home screen
    """
    return render(request, 'index.html')


@login_required()
def ajax_city_from_zip(request, zip):
    """
    todo: finish implementation
    :param request: client request
    :param zip: zip code of city
    :return:
    """
    cities = get_city_from_zip(zip)


@login_required()
def get_city_from_zip(zip):
    """
    :param zip:
    :return: city to entered zip
    """
    return City.objects.filter(zip_code=zip)


@login_required()
def add_member(request):
    """
    Loads the add member page. If there is a post registered to this view, then new member
    date will be verified and saved to the database.
    :param request: client request
    :return: add member page
    """
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
            #            user.member.city = city  # todo fix or delete
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
    """
    loads new "user for application" form
    :param request: client request
    :return: sign up form page
    """
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
    """
    Views all Members
    :param request: client request
    :return: page with a list of members
    """
    members = Member.objects.all()
    return render(request, 'list_members.html', {
        'members': members
    })


@login_required()
def list_member(request, member_id):
    """
    Shows a page with details of one user
    :param request: client request
    :param member_id: database id of particular user
    :return: page with user details
    """
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
    """
    Deletes a member in the system
    :param request: client request
    :param member_id: database id of particular user
    :return: Success message or a human readable error message
    """
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
    """
    Edit a profile of one selected member
    :param request: client request
    :param member_id: database id of particular user
    :return: page with loaded current member data or a success message or a error message if input are not OK
    """
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
    """
    Page for creating invoices.
    :param request: client request
    :return: page with form for creating a invoice
    """
    if request.method == 'POST':
        form = CreateInvoiceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            member = form.cleaned_data['member']
            # member_obj = User.objects.get(username=member)
            # member_id = member_obj.id
            # todo: clean list of members
            amount = form.cleaned_data['amount']
            due_date = form.cleaned_data['due_date']
            create_date = datetime.date.today()

            invoice = Invoice.objects.create(title=title,
                                             description=description,
                                             member_id=member,
                                             amount=amount,
                                             create_date=create_date,
                                             due_date=due_date)
            invoice.save()
            messages.add_message(request, messages.SUCCESS, f'Invoice have been created')
            return redirect('create_invoice')
    else:
        form = CreateInvoiceForm()

    return render(request, 'create_invoice.html', {'form': form})


@login_required()
def list_invoices(request):
    """
    Loads all active invoices and displays it to the user
    :param request: client request
    :return: returns a page with all created invoices
    """
    invoices = Invoice.objects.all()
    return render(request, 'list_invoices.html', {
        'invoices': invoices
    })


@login_required()
def edit_invoice(request, invoice_id):
    """
    Provides a mask for editing a invoice
    :param request: client request
    :param invoice_id: integer id of an invoice to edit
    :return: page with invoice edit mask
    """
    return render(request, 'edit_invoice.html')


def contact(request):
    """
    Shows App. contacts
    :param request: client request
    :return: page with contact details
    """
    return render(request, 'contact.html')


@login_required()
def list_ices(request):
    """
    List all booked ics slots
    :param request: client request
    :return: a page with a table of all ices
    """
    ice_slots = IceSlot.objects.all()
    return render(request, 'list_ices.html', {
        'ice_slots': ice_slots
    })


@login_required()
def add_ice(request):
    """
    Provides a form so user can schedule ice times
    :param request: client request
    :return: a page with add ice form
    """
    if request.method == 'POST':
        form = AddIceForm(request.POST)
        if form.is_valid():
            ice_slot = IceSlot(
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                club=request.user.member.club
            )
            ice_slot.save()
            ice_slot.refresh_from_db()
            messages.add_message(request, messages.SUCCESS,
                                 f'Added ice_slot at {ice_slot.start_time} for club {ice_slot.club.name}')
            return redirect('list_ices')
    else:
        form = AddIceForm()
    return render(request, 'add_ice.html', {
        'form': form
    })


@login_required()
def edit_ice(request, ice_slot_id):
    """
    View to edit a booked ice slot. e.g. it's time.
    :param request: client request
    :param ice_slot_id: id of to be modified ice slot
    :return: a page with a edit ice form
    """
    return render(request, 'edit_ice.html')


@login_required()
def delete_ice(request, ice_slot_id):
    """
    URL to delete a provided ice slot id and redirect to list ices view.
    :param request: client request
    :param ice_slot_id: id of to be deleted ice slot
    :return: success message and redirect to ice slot list or throws a error message
    """
    if request.method != 'POST':
        return HttpResponseBadRequest()
    # TODO logic for deleting
    ice_slot = get_object_or_404(IceSlot, pk=ice_slot_id)
    ice_slot.delete()
    messages.add_message(request, messages.SUCCESS, f'Deleted ice_slot {ice_slot_id}')
    return redirect('list_ices')
    # return render(request, 'delete_ice.html')


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


@login_required()
def list_trainings(request):
    """
    Lists all created and assigned trainings
    :param request: client request
    :return: page with table of trainings
    """
    trainings = Training.objects.all()
    return render(request, 'list_trainings.html', {
        'trainings': trainings
    })


@login_required()
def view_training(request, training_id):
    """
    Views a specific training with it's details
    :param request: client request
    :param training_id: integer id of to be viewed training
    :return: page displaying one training
    """
    return render(request, 'view_training.html')


@login_required()
def add_training(request):
    """
    Adds a training to a available ice slot
    :param request: client request
    :return: page with add training form
    """
    if request.method == 'POST':
        form = AddTrainingForm(request.POST)
        messages.add_message(request, messages.SUCCESS,
                             f'Added ice_slot at {ice_slot.start_time} for club {ice_slot.club.name}')
        return redirect('list_ices')
    else:
        form = AddTrainingForm(club=request.user.member.club)
    return render(request, 'add_training.html', {
        'form': form
    })


@login_required()
def edit_training(request, training_id):
    """
    Gives a mask to edit one particular training
    :param request: client request
    :param training_id: integer id of to be edited training
    :return: page with edit training mask
    """
    return render(request, 'edit_training.html')


@login_required()
def delete_training(request, training_id):
    """
    Deletes a training from a ice slot
    :param request: client request
    :param training_id: integer id of to be deleted training
    :return: success or error message
    """
    if request.method != 'POST':
        return HttpResponseBadRequest()
    # TODO logic for deleting
    training = get_object_or_404(Training, pk=training_id)
    training.delete()
    messages.add_message(request, messages.SUCCESS, f'Delete training {training_id}')
    return HttpResponse(status=204)
    # return render(request, 'delete_training.html')
