from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import DatabaseError
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger(__name__)


class EmailBackend(ModelBackend):
    """
    Custom authentication backend for email authentication.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if not email or not password:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        except DatabaseError:
            logger.error("A database error occurred.")
            raise ValidationError(_("A database error occurred."))
        except Exception as e:
            logger.error(f"An unknown error occurred. {e}")
            raise ValidationError(_("An unknown error occurred."))

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
