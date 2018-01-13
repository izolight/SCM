from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext

from main_app.forms import AddIceForm
from main_app.models import IceSlot


@login_required()
def list_ices(request):
    """
    List all booked ics slots
    :param request: client request
    :return: a page with a table of all ices
    """
    ice_slots = IceSlot.objects.all()
    return render(request, 'ice_slots/list_ices.html', {
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
                                 gettext('Added ice-slot at {start} for club {club}').format(start=ice_slot.start_time,
                                                                                             club=ice_slot.club.name))
            return redirect('list_ices')
    else:
        form = AddIceForm()
    return render(request, 'ice_slots/add_ice.html', {
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
    ice_slot = get_object_or_404(IceSlot, pk=ice_slot_id)
    if request.method == 'POST':
        form = AddIceForm(request.POST, instance=ice_slot)
        if form.is_valid():
            old_start = ice_slot.start_time
            old_end = ice_slot.end_time
            ice_slot = form.save(commit=False)
            ice_slot.save()
            messages.add_message(request, messages.SUCCESS,
                                 gettext(
                                     'Changed time from {old_start}-{old_end} to {start}-{end} for slot {id}').format(
                                     old_start=old_start, old_end=old_end, start=ice_slot.start_time,
                                     end=ice_slot.end_time, id=ice_slot_id))
            return redirect('list_ices')
    else:
        form = AddIceForm(instance=ice_slot)
    return render(request, 'ice_slots/add_ice.html', {
        'form': form,
    })


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
    messages.add_message(request, messages.SUCCESS, gettext('Deleted ice_slot {id}').format(id=ice_slot_id))
    return redirect('list_ices')
