import logging
import jdatetime
from datetime import datetime, date

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

logger = logging.getLogger(__name__)


def to_jalali(input_date, output_format='%Y-%m-%d'):
    """
    Converts a Gregorian date to Jalali (Shamsi) and returns it as a string in the specified format.
    """

    if not input_date:
        return _("N/A")

    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, '%Y-%m-%d').date()
    elif isinstance(input_date, datetime):
        input_date = input_date.date()

    if not isinstance(input_date, date):
        raise ValueError("input_date must be a datetime, date, or string in 'YYYY-MM-DD' format")

    jalali_date = jdatetime.date.fromgregorian(date=input_date)

    return jalali_date.strftime(output_format)


def is_admin(user):
    """
    Checks if the user is an admin.
    """
    return user.is_superuser or user.is_staff or user.groups.filter(name="admin").exists()


def toast(request, message, level="info"):
    """
    Adds a flash message to the request. Supports both string and dictionary message types.

    :param request: HttpRequest object.
    :param message: The message content. Can be a string or a dictionary for field errors.
    :param level: The level of the message (e.g., 'info', 'success', 'warning', 'error').
    """
    valid_levels = {
        'debug': messages.DEBUG,
        'info': messages.INFO,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR
    }

    if level not in valid_levels:
        logger.error(f"Invalid message level: {level}")
        raise ValueError(_(f"Invalid message level: {level}"))

    message_level = valid_levels[level]

    if isinstance(message, dict):
        for field_name, error_list in message.items():
            for error in error_list:
                messages.add_message(request, message_level, f"{field_name}: {error}")
    elif isinstance(message, str):
        messages.add_message(request, message_level, message)
    else:
        logger.error(f"Unsupported message type: {type(message)}")
        raise ValueError(_(f"Unsupported message type: {type(message)}"))
