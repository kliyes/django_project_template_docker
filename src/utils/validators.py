from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _, ungettext_lazy


PHONE_NUMBER_REGEX = r'^1[3|4|5|7|8|9][0-9]{9}$'


@deconstructible
class PhoneNumberRegexValidator(validators.RegexValidator):
    regex = PHONE_NUMBER_REGEX
    message = _('Enter a valid mobile phone number.')


class ExplicitLengthValidator(validators.BaseValidator):
    message = ungettext_lazy(
        'Ensure this value has explicitly %(limit_value)d character (it has %(show_value)d).',
        'Ensure this value has explicitly %(limit_value)d characters (it has %(show_value)d).',
        'limit_value')
    code = 'explicit_length'

    def compare(self, a, b):
        return not a == b

    def clean(self, x):
        return len(x)


class MaxFileSizeValidator(validators.BaseValidator):
    message = _("Ensure file size is less than or equal to %(limit_value)d bytes (it has %(show_value)d).")
    code = "max_file_size"

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return x.size


def validate_id_card_num(value):
    """
    Validate ID Card number
    Ref: https://my.oschina.net/jhao104/blog/756241

    :param value: string number
    :return:
    """
    length = len(value)
    if not length == 18:
        raise ValidationError(_("ID Card number Length must be 18"))
    total = 0
    for index, char in enumerate(value[:17], 1):
        total += int(char) * ((2 ** (length - index)) % 11)

    check_list = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    if not value[17].upper() == check_list[total % 11]:
        raise ValidationError(_("Invalid ID Card number: %s") % value)
