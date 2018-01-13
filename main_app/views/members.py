from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext

from main_app.forms import EditMemberForm, AddMemberForm
from main_app.models import Member, City


@login_required()
def list_members(request):
    """
    Views all Members
    :param request: client request
    :return: page with a list of members
    """
    members = Member.objects.all()
    return render(request, 'members/list_members.html', {
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
    return render(request, 'members/list_member.html', {
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
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    messages.add_message(request, messages.SUCCESS, gettext('Deleted member {member_id}').format(member_id=member_id))
    return redirect('list_members')


@login_required()
def edit_member(request, member_id):
    """
    Edit a profile of one selected member
    :param request: client request
    :param member_id: database id of particular user
    :return: page with loaded current member data or a success message or a error message if input are not OK
    """
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        form = EditMemberForm(request.POST, member=member)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 gettext('Edited Member {member_id} successfully').format(member_id=member_id))
        return redirect('list_members')
    else:
        form = EditMemberForm(member=member)
    return render(request, 'members/edit_member.html', {
        'form': form
    })


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
            user, password = create_member(form)
            messages.add_message(request, messages.SUCCESS,
                                 gettext('Added member {first_name} {last_name}').format(first_name=user.first_name,
                                                                                         last_name=user.last_name))
            return redirect('list_members')
    else:
        form = AddMemberForm()
    return render(request, 'members/add_member.html', {
        'form': form
    })


def create_member(form):
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
    db_city = City.objects.filter(name=city).filter(zip_code=zip_code).first()
    if db_city is None:
        db_city = City.objects.create(name=city, zip_code=zip_code)
        db_city.save()
        db_city.refresh_from_db()
    user.member.city = db_city
    user.member.phone_number = phone_number
    user.save()

    return user, password


def signup(request):
    """
    loads new "user for application" form
    :param request: client request
    :return: sign up form page
    """
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user, password = create_member(form)
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('loggedInLandingPage')
    else:
        form = AddMemberForm()
    return render(request, 'members/add_member.html', {
        'form': form
    })


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
