# Streamverse Redirect Gateway

Pagina local hecha con Django para funcionar como puerta de redireccion. El usuario captura nombre, correo y numero telefonico, recibe un codigo de verificacion simulado, lo ingresa y despues pasa a una pantalla que redirige al destino configurado.

## Que incluye

- Login sencillo con nombre, correo y telefono.
- Autenticacion en 2 pasos con codigo de 6 digitos.
- Simulacion de envio por correo y SMS.
- Pantalla de redireccion con cuenta regresiva.
- Interfaz con Tailwind CSS por CDN, CSS propio, botones transparentes, particulas suspendidas y animaciones al hacer scroll.
- Pagina local de destino: `/streamverse-demo/`.

## Como ejecutarlo

Usa Python 3.11 si esta disponible en Windows:

```powershell
py -3.11 -m pip install -r requirements.txt
py -3.11 manage.py migrate
py -3.11 manage.py runserver 8046
```

Despues abre:

```text
http://127.0.0.1:8046/
```

## Como funciona el flujo

1. El usuario entra al login y escribe nombre, correo y telefono.
2. Django genera un codigo de 6 digitos y lo guarda temporalmente en la sesion.
3. Como esta version es local, el codigo aparece en el mensaje de pantalla y tambien se imprime en la consola del servidor.
4. El usuario escribe el codigo en `/verificar/`.
5. Si el codigo es correcto y no expiro, se marca la sesion como verificada.
6. El sistema muestra `/redirigiendo/` y manda al usuario al destino configurado.

## Cambiar la pagina destino

Actualmente el destino esta en `redirector/settings.py`:

```python
LOGIN_REDIRECT_TARGET = '/streamverse-demo/'
```

Puedes reemplazarlo por una URL real:

```python
LOGIN_REDIRECT_TARGET = 'https://tu-dominio.com/'
```

## Importante sobre correo y SMS

Esta demo no envia correos ni mensajes reales porque no esta conectada a un proveedor externo. Para produccion necesitarias integrar servicios como:

- Email: SMTP, SendGrid, Mailgun, Amazon SES.
- SMS: Twilio, Vonage, MessageBird u otro proveedor.

La vista `gateway/views.py` ya tiene el punto donde se genera el codigo. Ahi se conectarian las llamadas reales de email y SMS.

## Pruebas

```powershell
py -3.11 manage.py test
```
