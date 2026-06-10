import random
from .models import SolicitudAcceso
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone


def _mask_email(email):
    name, _, domain = email.partition('@')
    if not domain:
        return email
    visible = name[:2] if len(name) > 2 else name[:1]
    return f'{visible}***@{domain}'


def _mask_phone(phone):
    clean = ''.join(char for char in phone if char.isdigit())
    if len(clean) <= 4:
        return '***'
    return f'*** *** {clean[-4:]}'


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()

        if not name or '@' not in email or len(''.join(ch for ch in phone if ch.isdigit())) < 10:
            messages.error(request, 'Revisa tu nombre, correo y numero telefonico.')
            return render(request, 'gateway/login.html')

        SolicitudAcceso.objects.create(nombre=name, correo=email, telefono=phone)
        code = f'{random.randint(100000, 999999)}'
        request.session['pending_user'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'code': code,
            'expires_at': (timezone.now() + timedelta(minutes=5)).isoformat(),
        }

        print(f'[Streamverse Redirector] Codigo 2FA simulado para {email} / {phone}: {code}')
        messages.success(
            request,
	f'Tu solicitud fue recibida. En breve recibirás confirmación.',
        )
        return redirect('verify')

    return render(request, 'gateway/login.html')


def verify_view(request):
    pending_user = request.session.get('pending_user')
    if not pending_user:
        messages.info(request, 'Primero registra tus datos para generar un codigo.')
        return redirect('login')

    if request.method == 'POST':
        typed_code = request.POST.get('code', '').strip()
        expires_at = timezone.datetime.fromisoformat(pending_user['expires_at'])

        if timezone.now() > expires_at:
            request.session.pop('pending_user', None)
            messages.error(request, 'El codigo expiro. Solicita uno nuevo.')
            return redirect('login')

        if typed_code != pending_user['code']:
            messages.error(request, 'Codigo incorrecto. Intentalo otra vez.')
        else:
            request.session['verified_user'] = {
                'name': pending_user['name'],
                'email': pending_user['email'],
                'phone': pending_user['phone'],
            }
            request.session.pop('pending_user', None)
            return redirect('redirecting')

    return render(
        request,
        'gateway/verify.html',
        {
            'email': _mask_email(pending_user['email']),
            'phone': _mask_phone(pending_user['phone']),
        },
    )


def redirecting_view(request):
    verified_user = request.session.get('verified_user')
    if not verified_user:
        messages.info(request, 'Completa la autenticacion para continuar.')
        return redirect('login')

    return render(
        request,
        'gateway/redirecting.html',
        {
            'user': verified_user,
            'target_url': settings.LOGIN_REDIRECT_TARGET,
        },
    )


def streamverse_demo_view(request):
    return render(request, 'gateway/demo_destination.html')

# Create your views here.
