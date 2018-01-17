from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext
from django.views.decorators.http import require_http_methods

from main_app.forms import AddTrainingForm
from main_app.models import Training


@require_http_methods(["GET"])
@login_required()
def list_trainings(request):
    """
    Lists all created and assigned trainings
    :param request: client request
    :return: page with table of trainings
    """
    club = request.user.member.club
    trainings = Training.objects.filter(club=club)
    return render(request, 'trainings/list_trainings.html', {
        'trainings': trainings
    })


@require_http_methods(["GET"])
@login_required()
def view_training(request, training_id):
    """
    Views a specific training with it's details
    :param request: client request
    :param training_id: integer id of to be viewed training
    :return: page displaying one training
    """
    training = get_object_or_404(Training, pk=training_id)
    return render(request, 'trainings/view_training.html', {'training': training})


@require_http_methods(["GET", "POST"])
@login_required()
def add_training(request):
    """
    Adds a training to a available ice slot
    :param request: client request
    :return: page with add training form
    """
    if request.method == 'POST':
        form = AddTrainingForm(request.POST, club=request.user.member.club)
        if form.is_valid():
            training = Training(
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                club=request.user.member.club,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            training.save()
            training.refresh_from_db()
            training.ice_slot = form.cleaned_data['ice_slot']
            training.members = form.cleaned_data['members']
            training.trainer = form.cleaned_data['trainer']
            training.save()
            training.refresh_from_db()

            messages.add_message(request, messages.SUCCESS,
                                 gettext('Added training at {start} for club {club}').format(start=training.start_time,
                                                                                             club=training.club.name))
            return redirect('list_trainings')
    else:
        form = AddTrainingForm(club=request.user.member.club)
    return render(request, 'trainings/add_training.html', {
        'form': form
    })


@require_http_methods(["GET", "POST"])
@login_required()
def edit_training(request, training_id):
    """
    Gives a mask to edit one particular training
    :param request: client request
    :param training_id: integer id of to be edited training
    :return: page with edit training mask
    """
    training = get_object_or_404(Training, pk=training_id)
    if request.method == 'POST':
        form = AddTrainingForm(request.POST, club=request.user.member.club, instance=training)
        if form.is_valid():
            form.save()
            return redirect('list_trainings')
    else:
        form = AddTrainingForm(club=request.user.member.club, instance=training)
    return render(request, 'trainings/add_training.html', {
        'form': form
    })


@require_http_methods(["POST"])
@login_required()
def delete_training(request, training_id):
    """
    Deletes a training from a ice slot
    :param request: client request
    :param training_id: integer id of to be deleted training
    :return: success or error message
    """
    if request.method == 'POST':
        training = get_object_or_404(Training, pk=training_id)
        training.delete()
        messages.add_message(request, messages.SUCCESS,
                             gettext('Deleted training {training_id}').format(training_id=training_id))
        return redirect('list_trainings')


@require_http_methods(["POST"])
@login_required()
def unregister_from_training(request, training_id):
    if request.method == 'POST':
        training = get_object_or_404(Training, pk=training_id)
        training.members.remove(request.user.member)
        training.save()
        training.refresh_from_db()
        messages.add_message(request, messages.SUCCESS,
                             gettext('Unregistered from training'))
        return redirect('view_training', training_id=training_id)