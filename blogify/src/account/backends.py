from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

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

        except UserModel.IdentityByEmailDoesNotExist as e:
            logger.error(e)
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.authenticate_phone(phone=username)
            if user.check_password(password):
                return user

        except UserModel.IdentityByPhoneDoesNotExist as e:
            logger.error(e)
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
