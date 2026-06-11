from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone


def _mask_phone(phone):
    clean = ''.join(c for c in phone if c.isdigit())
    if len(clean) <= 4:
        return '***'
    return f'*** *** {clean[-4:]}'


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()

        if not name or '@' not in email or len(''.join(c for c in phone if c.isdigit())) < 10:
            messages.error(request, 'Revisa tu nombre, correo y numero de WhatsApp.')
            return render(request, 'gateway/login.html')

        from django.db import connection
        now = timezone.now()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO paneladmin_accessrequest
                    (name, email, whatsapp, status, access_code, source, notes, created_at, updated_at)
                VALUES (%s, %s, %s, 'pending', '', 'Formulario projectgp.online/acceso', '', %s, %s)
                """,
                [name, email, phone, now, now],
            )

        return render(request, 'gateway/solicitud_enviada.html', {
            'name': name,
            'phone_masked': _mask_phone(phone),
        })

    return render(request, 'gateway/login.html')
