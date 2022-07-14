import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator(object):
    """ Validates whether the password has 1 digit. """
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least %(min_digits)d digit, 0-9."),
                code='password_no_number',
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    """ Validated whether the password has one uppercase letter. """

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )
