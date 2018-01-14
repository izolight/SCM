from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext
from django.views.decorators.http import require_http_methods

from main_app.forms import CreateInvoiceForm
from main_app.models import Invoice


@require_http_methods(["GET", "POST"])
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
            invoice = Invoice(form.instance)
            invoice.save()
            invoice.refresh_from_db()
            messages.add_message(request, messages.SUCCESS,
                                 gettext('Created {invoice_title} for club {club}').format(invoice_title=invoice.title,
                                                                                           club=invoice.club.name))
            return redirect('list_invoices')
    else:
        form = CreateInvoiceForm(club=request.user.member.club)
    return render(request, 'invoices/create_invoice.html', {
        'form': form
    })


@require_http_methods(["GET"])
@login_required()
def list_invoices(request):
    """
    Loads all active invoices and displays it to the user
    :param request: client request
    :return: returns a page with all created invoices
    """
    invoices = Invoice.objects.all()
    return render(request, 'invoices/list_invoices.html', {
        'invoices': invoices
    })


@require_http_methods(["GET", "POST"])
@login_required()
def edit_invoice(request, invoice_id):
    """
    Provides a mask for editing a invoice
    :param request: client request
    :param invoice_id: integer id of an invoice to edit
    :return: page with invoice edit mask
    """
    return render(request, 'invoices/edit_invoice.html')
