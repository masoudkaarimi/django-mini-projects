from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from loan.forms import LoanAdminForm, InstallmentAdminForm
from loan.models import Loan, Installment, InstallmentPayment


# Register your models here.

class LoanAdmin(admin.ModelAdmin):
    add_form = LoanAdminForm
    form = LoanAdminForm
    list_display = ['id', 'number', 'name', 'user', 'amount', 'interest_rate', 'installment_choice', 'installment_count', 'start_date']
    fieldsets = [
        [_("Loan Information"), {"fields": ["user", "number", "name", "amount", "interest_rate", "installment_choice", "installment_count", "start_date"]}],
    ]
    readonly_fields = ["number", "start_date"]


class InstallmentAdmin(admin.ModelAdmin):
    add_form = InstallmentAdminForm
    form = InstallmentAdminForm
    list_display = ['id', 'number', 'loan', 'due_date', 'amount', 'status', 'description']
    fieldsets = [
        [_("Installment Information"), {'fields': ['loan', 'number', 'due_date', 'amount', 'status', 'description']}],
    ]
    readonly_fields = ["due_date", "amount", 'number']


class InstallmentPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'installment', 'description', 'paid_at', 'create_at', 'update_at']
    readonly_fields = ["paid_at"]


admin.site.register(Loan, LoanAdmin)
admin.site.register(Installment, InstallmentAdmin)
admin.site.register(InstallmentPayment, InstallmentPaymentAdmin)
