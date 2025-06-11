from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

import logging

logger = logging.getLogger(__name__)


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.authenticate_email(email=username)
            if user.check_password(password):
                return user
            return None

        except UserModel.IdentityByEmailDoesNotExist as e:
            logger.error(e)
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.authenticate_phone_number(phone_number=username)
            if user.check_password(password):
                return user
            return None

        except UserModel.IdentityByPhoneNumberDoesNotExist as e:
            logger.error(e)
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
