from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext
from django.views.decorators.http import require_http_methods

from main_app.forms import EditMemberForm, AddMemberForm
from main_app.models import Member, City


@require_http_methods(["GET"])
@login_required()
def list_members(request):
    """
    Views all Members
    :param request: client request
    :return: page with a list of members
    """
    club = request.user.member.club
    members = Member.objects.filter(club=club)
    return render(request, 'members/list_members.html', {
        'members': members
    })


@require_http_methods(["GET"])
@login_required()
def list_member(request, member_id):
    """
    Shows a page with details of one user
    :param request: client request
    :param member_id: database id of particular user
    :return: page with user details
    """
    member = get_object_or_404(Member, pk=member_id)
    return render(request, 'members/list_member.html', {
        'member': member
    })


@require_http_methods(["POST"])
@login_required()
def delete_member(request, member_id):
    """
    Deletes a member in the system
    :param request: client request
    :param member_id: database id of particular user
    :return: Success message or a human readable error message
    """
    if request.method == 'POST':
        club = request.user.member.club
        member = get_object_or_404(Member, pk=member_id, club=club)
        member.delete()
        messages.add_message(request, messages.SUCCESS,
                             gettext('Deleted member {member_id}').format(member_id=member_id))
        return redirect('list_members')


@require_http_methods(["GET", "POST"])
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
            if form.has_changed():
                member.user.first_name = form.cleaned_data['first_name']
                member.user.last_name = form.cleaned_data['last_name']
                member.user.email = form.cleaned_data['email']
                member.address = form.cleaned_data['address']
                member.city = check_for_city(form.cleaned_data['city'], form.cleaned_data['zip_code'])
                member.phone_number = form.cleaned_data['phone_number']
                member.save()
            messages.add_message(request, messages.SUCCESS,
                                 gettext('Edited Member {member_id} successfully').format(member_id=member_id))
            return redirect('list_members')
    else:
        form = EditMemberForm(member=member)
    return render(request, 'members/edit_member.html', {
        'form': form
    })


@require_http_methods(["GET", "POST"])
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
    """
    Helper function that is used by the signup and add_member form
    :param form: the form from the request
    :return: user object and password
    """
    password = form.cleaned_data['password1']
    user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                                    last_name=form.cleaned_data['last_name'],
                                    username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=password)
    user.save()
    user.refresh_from_db()
    user.member.city = check_for_city(form.cleaned_data['city'], form.cleaned_data['zip_code'])
    user.member.address = form.cleaned_data['address']
    user.member.phone_number = form.cleaned_data['phone_number']
    user.member.club = form.cleaned_data['club']
    user.save()

    return user, password


def check_for_city(city, zip_code):
    """
    Helper function to check if a city exists in the db and creates it if necessary
    :param city: cityname
    :param zip_code: corresponding zip code
    :return: city object
    """
    db_city = City.objects.filter(name=city).filter(zip_code=zip_code).first()
    if db_city is None:
        db_city = City.objects.create(name=city, zip_code=zip_code)
        db_city.save()
        db_city.refresh_from_db()
    return db_city


@require_http_methods(["GET", "POST"])
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
