from django.shortcuts import render, redirect, get_object_or_404
from .models import Manufacturer, Case, UnknownCase, Message
from .forms import UnknownCaseForm, MessageForm


def index(request):
    cases = Case.objects.all().select_related('manufacturer')
    manufacturers = Manufacturer.objects.all()
    return render(request, 'cases/index.html', {
        'cases': cases,
        'manufacturers': manufacturers
    })


def manufacturer_detail(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
    cases = manufacturer.cases.all()
    manufacturers = Manufacturer.objects.all()
    return render(request, 'cases/manufacturer_detail.html', {
        'manufacturer': manufacturer,
        'cases': cases,
        'manufacturers': manufacturers
    })


def unknown_list(request):
    unknown_cases = UnknownCase.objects.all().order_by('-created_at')
    manufacturers = Manufacturer.objects.all()
    return render(request, 'cases/unknown_list.html', {
        'unknown_cases': unknown_cases,
        'manufacturers': manufacturers
    })


def unknown_create(request):
    manufacturers = Manufacturer.objects.all()

    if request.method == 'POST':
        form = UnknownCaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('unknown_list')
    else:
        form = UnknownCaseForm()

    return render(request, 'cases/unknown_form.html', {
        'form': form,
        'manufacturers': manufacturers
    })


def unknown_detail(request, unknown_id):
    unknown_case = get_object_or_404(UnknownCase, id=unknown_id)
    manufacturers = Manufacturer.objects.all()
    messages = unknown_case.messages.all().order_by('-created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.unknown_case = unknown_case
            message.save()
            return redirect('unknown_detail', unknown_id=unknown_case.id)
    else:
        form = MessageForm()

    return render(request, 'cases/unknown_detail.html', {
        'unknown_case': unknown_case,
        'messages': messages,
        'form': form,
        'manufacturers': manufacturers
    })


def add_message(request, unknown_id):
    unknown_case = get_object_or_404(UnknownCase, id=unknown_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        if name and message:
            Message.objects.create(
                unknown_case=unknown_case,
                name=name,
                message=message
            )
    return redirect('unknown_list')


def delete_unknown(request, unknown_id):
    unknown_case = get_object_or_404(UnknownCase, id=unknown_id)
    unknown_case.delete()
    return redirect('unknown_list')
