from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("Email address"),
        help_text=_("Required. This will be used as the user's email address.")
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
        help_text=_('Optional. Contact number for the user if provided.')
    )
    last_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("Last IP Address"),
        help_text=_("IP address of the user's last login, if available.")
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('loan:user_detail', kwargs={'pk': self.pk})

    def get_fullname(self):
        if not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.last_name}"

    def get_total_loans(self):
        """
        Gets the total number of loans for the user.
        """
        return self.user_loan.count()

    def get_total_loans_amount(self):
        """
        Gets the total amount of the user's loans.
        """
        return self.user_loan.aggregate(x=Sum('amount'))["x"] or 0

    def get_total_installments_paid(self):
        """
        Gets the total number of paid installments for the user's loans.
        """
        return self.user_loan.filter(loan_installment__status='paid').count()

    def get_total_installments_paid_amount(self):
        """
        Gets the total amount of paid installments for the user's loans.
        """
        return self.user_loan.filter(loan_installment__status='paid').aggregate(x=Sum('loan_installment__amount'))["x"] or 0

    def get_total_installments_unpaid(self):
        """
        Gets the total number of unpaid installments for the user's loans.
        """
        return self.user_loan.filter(loan_installment__status='unpaid').count()

    def get_total_installments_unpaid_amount(self):
        """
        Gets the total amount of unpaid installments for the user's loans.
        """
        return self.user_loan.filter(loan_installment__status='unpaid').aggregate(x=Sum('loan_installment__amount'))["x"] or 0

    def get_total_loans_interest_rate_amount(self):
        """
        Gets the total amount of interest rates for the user's loans.
        """
        # total_interest_amount = 0
        # for loan in self.user_loan.all():
        #     total_interest_amount += (loan.amount * loan.interest_rate) / 100
        # return int(total_interest_amount)

        total_interest = self.user_loan.aggregate(x=Sum(F('amount') * F('interest_rate') / 100))["x"] or 0
        return int(total_interest)
