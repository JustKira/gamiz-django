from django.core.mail import EmailMessage, EmailMultiAlternatives
import threading
from django.template.loader import render_to_string
from django.conf import settings


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:

    @staticmethod
    def send_email(data):

        msg_txt = render_to_string(
            'email.txt', {'verify_url': data["verify_url"], 'user': data["user"]})
        msg_html = render_to_string(
            'email.html', {'verify_url': data["verify_url"], 'user': data["user"]})

        email = EmailMultiAlternatives(
            subject=data['email_subject'], body=msg_txt, from_email=settings.EMAIL_HOST_USER, to=[data['to_email']])
        email.attach_alternative(msg_html, "text/html")
        EmailThread(email).start()
