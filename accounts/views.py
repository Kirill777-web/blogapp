from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


class CustomConfirmEmailView(TemplateView):
    template_name = "account/email_confirm.html"

    def get(self, request, key, *args, **kwargs):
        logger.debug(f"Received key: {key}")
        confirmation = self.get_confirmation_object(key)
        if confirmation:
            confirmation.confirm(request)
            logger.debug("Email address confirmed.")
            return render(request, self.template_name, {"message": "Email address confirmed."})
        logger.debug("Invalid key.")
        return render(request, self.template_name, {"message": "Invalid key."})

    def get_confirmation_object(self, key):
        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
            if confirmation:
                return confirmation
        except EmailConfirmation.DoesNotExist:
            pass
        try:
            confirmation = EmailConfirmation.objects.get(key=key)
            return confirmation
        except EmailConfirmation.DoesNotExist:
            return None
