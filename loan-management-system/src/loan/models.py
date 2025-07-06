from datetime import timedelta

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import Sum, Max
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import to_jalali


class Loan(models.Model):
    INSTALLMENT_CHOICES = (
        ('0', _('Custom')),
        ('3', _('3 Monthly')),
        ('6', _('6 Monthly')),
        ('12', _('12 Monthly')),  # 1 year
        ('24', _('24 Monthly')),  # 2 years
        ('36', _('36 Monthly')),  # 3 years
        ('48', _('48 Monthly')),  # 4 years
        ('60', _('60 Monthly')),  # 5 years
    )

    user = models.ForeignKey(
        get_user_model(),
        related_name="user_loan",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_("Loan Owner"),
        help_text=_("The user to whom this loan belongs.")
    )
    number = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Loan Number"),
        help_text=_("A unique loan identification number.")
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_("Loan Name"),
        help_text=_("A descriptive name for the loan.")
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
        verbose_name=_("Loan Amount"),
        help_text=_("The principal amount of the loan.")
    )
    interest_rate = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Interest Rate (%)"),
        help_text=_("The interest rate applied to the loan.")
    )
    installment_choice = models.CharField(
        max_length=2,
        choices=INSTALLMENT_CHOICES,
        default='3',
        verbose_name=_("Installment Plan"),
        help_text=_("Choose a loan repayment installment plan.")
    )
    installment_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Installment Count"),
        help_text=_("The number of installments for the loan repayment.")
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Start Date"),
        help_text=_("The date when the loan period starts.")
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created.")
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated.")
    )

    class Meta:
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")
        ordering = ['-id']
        # unique_together = ('user', 'number')

    def __str__(self):
        return f"{self.user.username}: {self.name}"

    def get_absolute_url(self):
        return reverse("loan:loan_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.number is None:
            with transaction.atomic():
                max_number = Loan.objects.aggregate(max_number=Max('number'))['max_number'] or 0
                self.number = max_number + 1

        super().save(*args, **kwargs)

        installment_count = self.get_installment_count()

        if self.installment_choice != '0':
            installment_count = int(self.installment_choice)

        amount = (self.amount + (self.amount * (self.interest_rate / 100))) / installment_count

        for i in range(installment_count):
            due_date = self.start_date + timedelta(days=30 * (i + 1))
            description = f"Loan: {self.name}\nAmount: {round(amount, 2)}\nDue Date: {to_jalali(due_date)}\nInstallment: {i + 1}"
            Installment.objects.update_or_create(loan=self, due_date=due_date, defaults={"amount": amount, "description": description})

    def get_installment_count(self):
        """
        Calculates the total number of installments.
        """
        return int(self.installment_choice) if self.installment_choice != '0' else self.installment_count or 0

    def get_amount(self):
        """
        Calculates the total loan amount excluding interest.
        """
        return self.amount

    def get_total_paid(self):
        """
        Calculates the total paid amount.
        """
        return self.loan_installment.filter(status='paid').aggregate(total_paid=Sum("amount"))['total_paid'] or 0

    def get_total_unpaid(self):
        """
        Calculates the total unpaid amount.
        """
        return self.loan_installment.filter(status='unpaid').aggregate(total_unpaid=Sum("amount"))['total_unpaid'] or 0

    def get_end_date(self):
        """
        Calculates the expected end date of the loan.
        """
        return to_jalali(input_date=self.start_date + timedelta(days=30 * self.get_installment_count()), output_format='%Y/%m/%d')

    def get_repayment_amount(self):
        """
        Calculates the total repayment amount with loan interest.
        """
        # return self.get_amount() * (1 + (self.interest_rate / 100))
        # return self.get_amount() + ((self.interest_rate / 100) * self.get_total_amount())
        return self.loan_installment.aggregate(total_repayment_amount=Sum("amount"))['total_repayment_amount'] or 0


class Installment(models.Model):
    STATUS_CHOICES = (("paid", _("Paid")), ("unpaid", _("Unpaid")))

    loan = models.ForeignKey(
        Loan,
        related_name="loan_installment",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_("Associated Loan"),
        help_text=_("The loan to which this installment belongs.")
    )
    number = models.IntegerField(
        blank=False,
        null=False,
        verbose_name=_("Installment Number"),
        help_text=_("A unique installment identification number.")
    )
    due_date = models.DateTimeField(
        verbose_name=_("Due Date"),
        help_text=_("The date by which the installment must be paid.")
    )
    amount = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
        verbose_name=_("Installment Amount"),
        help_text=_("The specific amount due for this installment.")
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default='unpaid',
        verbose_name=_("Payment Status"),
        help_text=_("The current payment status of this installment.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Additional details or information about the installment.")
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created.")
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated.")
    )

    class Meta:
        ordering = ['due_date']
        unique_together = ['loan', 'due_date']

    def __str__(self):
        return f"{self.loan.user}: {self.loan.name} - Installment {self.number}"

    def save(self, *args, **kwargs):
        if self.number is None:
            with transaction.atomic():
                max_number = Installment.objects.filter(loan=self.loan).aggregate(max_number=Max('number'))['max_number'] or 0
                self.number = max_number + 1

        super().save(*args, **kwargs)

    # def get_amount_with_interest(self):
    #     """
    #     Calculates the installment amount with the loan interest.
    #     """
    #     return self.amount + ((self.loan.interest_rate / 100) * self.amount)


class InstallmentPayment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name="user_payment",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Payment Owner"),
        help_text=_("The user who made the payment.")
    )
    installment = models.ForeignKey(
        Installment,
        related_name="installment_payment",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Associated Installment"),
        help_text=_("The installment to which this payment belongs.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Additional details or information about the payment.")
    )
    paid_at = models.DateTimeField(
        verbose_name=_("Payment Date"),
        help_text=_("The date and time when the payment was made.")
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created.")
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated.")
    )

    class Meta:
        ordering = ['-create_at']
