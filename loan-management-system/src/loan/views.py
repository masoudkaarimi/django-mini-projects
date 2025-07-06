from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Count, Q, F
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.utils.translation import gettext as _

from account.models import User
from core.utils import toast
from loan.forms import LoanCreateForm, LoanUpdateForm,  UserCreateAdminForm, UserUpdateAdminForm
from loan.models import Loan, Installment, InstallmentPayment


@login_required(login_url="/login")
def dashboard_view(request, *args, **kwargs):
    user = request.user

    if user.is_staff:
        context = handle_admin_data(user)
    else:
        context = handle_user_data(user)

    return render(request, "dashboard/dashboard.html", context)


def handle_admin_data(user):
    try:
        loans = Loan.objects.prefetch_related()
        latest_loans = loans[:5]
        latest_users = User.objects.all()[:5]

        total_users = User.objects.filter(is_active=True).count()
        # total_loans = loans.count()
        # total_installments_paid = loans.filter(loan_installment__status='paid').count()
        # total_installments_unpaid = loans.filter(loan_installment__status='unpaid').count()
        # total_loans_amount = loans.aggregate(x=Sum('amount'))['x'] or 0
        # total_installments_paid_amount = loans.filter(loan_installment__status='paid').aggregate(x=Sum('loan_installment__amount'))['x'] or 0
        # total_installments_unpaid_amount = loans.filter(loan_installment__status='unpaid').aggregate(x=Sum('loan_installment__amount'))['x'] or 0
        # total_loans_interest_rate_amount = loans.aggregate(x=Sum('amount') * Sum('interest_rate') / 100)['x'] or 0

        # or

        queryset = loans.aggregate(
            total_loans=Count('id', distinct=True),
            total_installments_paid=Count('loan_installment', filter=Q(loan_installment__status='paid')),
            total_installments_unpaid=Count('loan_installment', filter=Q(loan_installment__status='unpaid')),
            total_loans_amount=Sum('amount', distinct=True),
            total_installments_paid_amount=Sum('loan_installment__amount', filter=Q(loan_installment__status='paid')),
            total_installments_unpaid_amount=Sum('loan_installment__amount', filter=Q(loan_installment__status='unpaid')),
            total_loans_interest_rate_amount=Sum(F('amount') * F('interest_rate') / 100, distinct=True)
        )

        context = {
            "stats": [
                {"title": _("Total Users"), "value": total_users, "unit": '', "bg_color": "bg-primary", "color": 'text-white'},
                {"title": _("Total Loans"), "value": queryset.get("total_loans"), "unit": '', "bg_color": "bg-info", "color": 'text-white'},
                {"title": _("Total Paid Installments"), "value": queryset.get("total_installments_paid"), "unit": '', "bg_color": "bg-success", "color": 'text-white'},
                {"title": _("Total Unpaid Installments"), "value": queryset.get("total_installments_unpaid"), "unit": '', "bg_color": "bg-secondary", "color": 'text-white'},

                {"title": _("Total Loans Amount"), "value": queryset.get("total_loans_amount"), "unit": _("Toman"), "bg_color": "bg-primary", "color": 'text-white'},
                {"title": _("Total Paid Installments Amount"), "value": queryset.get("total_installments_paid_amount"), "unit": _("Toman"), "bg_color": "bg-success",
                 "color": 'text-white'},
                {"title": _("Total Unpaid Installments Amount"), "value": queryset.get("total_installments_unpaid_amount"), "unit": _("Toman"), "bg_color": "bg-secondary",
                 "color": 'text-white'},
                {"title": _("Total Interest Rates Amount"), "value": queryset.get("total_loans_interest_rate_amount"), "unit": _("Toman"), "bg_color": "bg-warning",
                 "color": 'text-dark'},
            ],
            "title": _("Admin Dashboard"),
            "loans": latest_loans,
            "users": latest_users,
        }
        return context
    except Loan.DoesNotExist:
        pass
    except User.DoesNotExist:
        pass


def handle_user_data(user):
    try:
        # latest_loans = Loan.objects.filter(user=user).order_by('-create_at')[:5]
        # latest_loans = Loan.objects.filter(user=user)[:5]
        latest_loans = user.user_loan.all()[:5]
        context = {
            "stats": [
                {"title": _("Total Loans"), "value": user.get_total_loans, "unit": '', "bg_color": "bg-primary", "color": 'text-white'},
                {"title": _("Total Paid Installments"), "value": user.get_total_installments_paid, "unit": '', "bg_color": "bg-success", "color": 'text-white'},
                {"title": _("Total Unpaid Installments"), "value": user.get_total_installments_unpaid, "unit": '', "bg_color": "bg-secondary", "color": 'text-white'},

                {"title": _("Total Loans Amount"), "value": user.get_total_loans_amount(), "unit": _("Toman"), "bg_color": "bg-primary", "color": 'text-white'},
                {"title": _("Total Paid Installments Amount"), "value": user.get_total_installments_paid_amount(), "unit": _("Toman"), "bg_color": "bg-success",
                 "color": 'text-white'},
                {"title": _("Total Unpaid Installments Amount"), "value": user.get_total_installments_unpaid_amount(), "unit": _("Toman"), "bg_color": "bg-secondary",
                 "color": 'text-white'},
                {"title": _("Total Interest Rate Amount"), "value": user.get_total_loans_interest_rate_amount(), "unit": _("Toman"), "bg_color": "bg-warning",
                 "color": 'text-dark'},
            ],
            "title": _("User Dashboard"),
            "loans": latest_loans,
        }
        return context
    except Loan.DoesNotExist:
        pass
    except User.DoesNotExist:
        pass


@login_required(login_url="/login")
# Loan Resource
def loan_list_view(request, *args, **kwargs):
    try:
        user = request.user
        context = {
            "title": _("Loan List"),
        }

        if user.is_staff:
            context["loans"] = Loan.objects.all()
        else:
            # context["loans"] = Loan.objects.filter(user=user),
            context["loans"] = user.user_loan.all()

        return render(request, "dashboard/loans.html", context)
    except Loan.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def loan_detail_view(request, pk, *args, **kwargs):
    try:
        user = request.user
        context = {
            "title": _("Loan Detail"),
        }

        if user.is_staff:
            context["loan"] = Loan.objects.get(pk=pk)
        else:
            # context["loan"] = Loan.objects.get(user=user, pk=pk)
            context["loan"] = user.user_loan.get(pk=pk)

        return render(request, "dashboard/components/loan/loan-detail.html", context)
    except Loan.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def loan_create_view(request, *args, **kwargs):
    try:
        user = request.user
        form = LoanCreateForm()

        if request.method == "POST":
            form = LoanCreateForm(request.POST)

            if form.is_valid():
                loan = form.save(commit=False)
                loan.user = user
                loan.save()
                return redirect('loan:loan_list')
            else:
                toast(request, form.errors, level="error")

        context = {
            "title": _("Loan Create"),
            "form": form,
        }
        return render(request, "dashboard/components/loan/loan-create.html", context)
    except Loan.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def loan_update_view(request, pk, *args, **kwargs):
    try:
        user = request.user

        if user.is_staff:
            loan = Loan.objects.get(pk=pk)
        else:
            # context["loan"] = Loan.objects.get(user=user, pk=pk)
            loan = user.user_loan.get(pk=pk)

        form = LoanUpdateForm(instance=loan)

        if request.method == "POST":
            form = LoanUpdateForm(request.POST, instance=loan)

            if form.is_valid():
                form.save()
                return redirect('loan:loan_list')
            else:
                toast(request, form.errors, level="error")

        context = {
            "title": _("Loan Edit"),
            "loan": loan,
            "form": form,
        }
        return render(request, "dashboard/components/loan/loan-edit.html", context)
    except Loan.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def loan_delete_view(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user
        loan_id = request.POST.get('loan_id')

        try:
            if user.is_staff:
                loan = Loan.objects.get(pk=loan_id)
            else:
                # context["loan"] = Loan.objects.get(user=user, pk=loan_id)
                loan = user.user_loan.get(pk=loan_id)

            loan.loan_installment.all().delete()
            loan.delete()

            toast(request, _("Loan deleted successfully."), level="success")
            return redirect("loan:loan_list")
        except Loan.DoesNotExist:
            toast(request, _("Loan does not exist!"), level="error")
            return redirect("loan:loan_list")
    else:
        toast(request, _("Invalid request method!"), level="error")
        return redirect("loan:loan_list")


@login_required(login_url='/login')
def loan_installment_payment_view(request, *args, **kwargs):
    user = request.user
    loan_id = request.POST.get('loan_id')
    installment_ids = request.POST.getlist('installment_ids', [])
    payment_date = request.POST.get('payment_date')
    payment_description = request.POST.get('payment_description')

    try:
        if request.method == 'POST':
            if not loan_id:
                toast(request, _("loan id is required!"), level="error")
                return redirect('loan:loan_detail', pk=loan_id)
            if not payment_date:
                toast(request, _("payment date is required!"), level="error")
                return redirect('loan:loan_detail', pk=loan_id)

            with transaction.atomic():
                loan = get_object_or_404(Loan, id=loan_id)
                installments = loan.loan_installment.filter(id__in=installment_ids, status='unpaid')

                # installments.bulk_update(status='paid')

                for installment in installments:
                    installment.status = 'paid'
                    InstallmentPayment.objects.create(user=user, installment=installment, paid_at=payment_date, description=payment_description)
                    installment.save()

                toast(request, _("Installments paid successfully."), level="success")
                return redirect('loan:loan_detail', pk=loan_id)
        else:
            toast(request, _("Method not allowed!"), level="error")
            return redirect('loan:loan_detail', pk=loan_id)
    except Exception as e:
        print(e)  # Todo handle logging
        toast(request, _("Installments payment failed."), level="error")
        return redirect('loan:loan_detail', pk=loan_id)


@login_required(login_url="/login")
def user_list_view(request, *args, **kwargs):
    try:
        users = User.objects.all()
        context = {
            "title": _("User List"),
            "users": users,
        }

        return render(request, 'dashboard/users.html', context)
    except User.DoesNotExist:
        return render(request, '404.html', status=404)


@login_required(login_url="/login")
def user_detail_view(request, pk, *args, **kwargs):
    try:
        user = User.objects.get(pk=pk)
        context = {
            "title": _("User Detail"),
            "user": user
        }
        return render(request, 'dashboard/components/user/user-detail.html', context)
    except User.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def user_create_view(request, *args, **kwargs):
    try:
        form = UserCreateAdminForm()

        if request.method == "POST":
            form = UserCreateAdminForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('loan:user_list')
            else:
                toast(request, form.errors, level="error")

        context = {
            "title": _("User Create"),
            "form": form
        }
        return render(request, "dashboard/components/user/user-create.html", context)
    except User.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def user_update_view(request, pk, *args, **kwargs):
    try:
        user = User.objects.get(pk=pk)
        form = UserUpdateAdminForm(instance=user)

        if request.method == "POST":
            form = UserUpdateAdminForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                return redirect('loan:user_list')
            else:
                toast(request, form.errors, level="error")

        context = {
            "title": _("User Edit"),
            "user": user,
            "form": form,
        }
        return render(request, 'dashboard/components/user/user-edit.html', context)
    except User.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required(login_url="/login")
def user_delete_view(request, *args, **kwargs):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
            user.delete()

            toast(request, _("User deleted successfully."), level="success")
            return redirect("loan:user_list")
        except User.DoesNotExist:
            toast(request, _("User does not exist!"), level="error")
            return redirect("loan:user_list")
    else:
        toast(request, _("Invalid request method!"), level="error")
        return redirect("loan:user_list")
