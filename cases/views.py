from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Manufacturer, Case, UnknownCase, Message
from .forms import UnknownCaseForm, MessageForm


def index(request):
    cases = Case.objects.all().select_related('manufacturer').order_by('manufacturer__name', 'model_name')
    manufacturers = Manufacturer.objects.all().order_by('name')
    return render(request, 'cases/index.html', {
        'cases': cases,
        'manufacturers': manufacturers
    })


def manufacturer_detail(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
    cases = manufacturer.cases.all().order_by('model_name')
    manufacturers = Manufacturer.objects.all().order_by('name')
    return render(request, 'cases/manufacturer_detail.html', {
        'manufacturer': manufacturer,
        'cases': cases,
        'manufacturers': manufacturers
    })


def unknown_list(request):
    unknown_cases = UnknownCase.objects.all().order_by('-created_at')
    manufacturers = Manufacturer.objects.all().order_by('name')
    return render(request, 'cases/unknown_list.html', {
        'unknown_cases': unknown_cases,
        'manufacturers': manufacturers
    })


def unknown_create(request):
    manufacturers = Manufacturer.objects.all().order_by('name')

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
    manufacturers = Manufacturer.objects.all().order_by('name')
    messages_list = unknown_case.messages.all().order_by('-created_at')

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
        'messages': messages_list,
        'form': form,
        'manufacturers': manufacturers
    })


def add_message(request, unknown_id):
    unknown_case = get_object_or_404(UnknownCase, id=unknown_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        message_text = request.POST.get('message')
        if name and message_text:
            Message.objects.create(
                unknown_case=unknown_case,
                name=name,
                message=message_text
            )

            # Отправляем email админу
            subject = f'Новое сообщение о неизвестном корпусе #{unknown_case.id}'
            email_body = f'''
Отправитель: {name}
Сообщение: {message_text}

Корпус: #{unknown_case.id}
            '''

            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Сообщение отправлено! Спасибо за помощь.')
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                messages.error(request, f'Ошибка: {e}')
        else:
            messages.error(request, 'Заполните все поля.')
    return redirect('unknown_list')


def delete_unknown(request, unknown_id):
    unknown_case = get_object_or_404(UnknownCase, id=unknown_id)
    unknown_case.delete()
    return redirect('unknown_list')
