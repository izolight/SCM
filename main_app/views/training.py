from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.forms import AddTrainingForm
from main_app.models import Training


@login_required()
def list_trainings(request):
    """
    Lists all created and assigned trainings
    :param request: client request
    :return: page with table of trainings
    """
    trainings = Training.objects.all()
    return render(request, 'trainings/list_trainings.html', {
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
    return render(request, 'trainings/view_training.html')


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
                             f'Added training at {training.start_time} for club {training.club.name}')
        return redirect('list_trainings')
    else:
        form = AddTrainingForm(club=request.user.member.club)
    return render(request, 'trainings/add_training.html', {
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
    return render(request, 'trainings/edit_training.html')


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