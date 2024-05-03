from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
import hashlib
import hmac
import urllib.parse
import os


def send_confirmation_email(order):
    subject = f"Gracias por tu compra - #{order.id}"
    # Render HTML template
    html_message = render_to_string(
        "email/order_confirmation.html",
        {
            "order": order,
            "customer": order.customer,
            "pack": order.pack,
            "server_name": settings.SERVER_NAME,
        },
    )

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email]

    # Pass HTML content as message
    send_mail(subject, None, email_from, recipient_list, html_message=html_message)


def send_contact_email(contact):
    subject = f"Nuevo mensaje de contacto - {contact.name}"
    # Render HTML template
    html_message = render_to_string(
        "email/contact_confirmation.html",
        {
            "contact": contact,
            "server_name": settings.SERVER_NAME,
        },
    )

    email_from = settings.EMAIL_HOST_USER
    recipient_list = settings.CONTACT_EMAILS

    # Pass HTML content as message
    send_mail(subject, None, email_from, recipient_list, html_message=html_message)


def check_mp_signature(request):
    # Obtain the x-signature value from the header
    xSignature = request.headers.get("x-signature")
    xRequestId = request.headers.get("x-request-id")

    # Obtain Query params related to the request URL
    queryParams = urllib.parse.parse_qs(request.GET.urlencode())

    # Extract the "data.id" from the query params
    dataID = queryParams.get("data.id", [""])[0]

    # Separating the x-signature into parts
    parts = xSignature.split(",")

    # Initializing variables to store ts and hash
    ts = None
    hash = None

    # Iterate over the values to obtain ts and v1
    for part in parts:
        # Split each part into key and value
        keyValue = part.split("=", 1)
        if len(keyValue) == 2:
            key = keyValue[0].strip()
            value = keyValue[1].strip()
            if key == "ts":
                ts = value
            elif key == "v1":
                hash = value

    # Obtain the secret key for the user/application from Mercadopago developers site
    secret = os.environ.get("MP_WEBHOOKS_SECRET_KEY")

    # Generate the manifest string
    manifest = f"id:{dataID};request-id:{xRequestId};ts:{ts};"

    # Create an HMAC signature defining the hash type and the key as a byte array
    hmac_obj = hmac.new(
        secret.encode(), msg=manifest.encode(), digestmod=hashlib.sha256
    )

    # Obtain the hash result as a hexadecimal string
    sha = hmac_obj.hexdigest()
    if sha == hash:
        # HMAC verification passed
        return True
    else:
        # HMAC verification failed
        return False
