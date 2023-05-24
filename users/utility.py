from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from users.models import Student, Sponsor


def sponsors_by_month():
    return Sponsor.manager.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id'))


def students_by_month():
    return Student.manager.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id'))


# jami to'langan summa
def total_amount_paid():
    return Student.manager.aggregate(Sum('amount_spent'))['amount_spent__sum']


# jami so'ralgan summa
def total_amount_requested():
    return Student.manager.aggregate(Sum('payment_amount'))['payment_amount__sum']


# kerakli summa
def amount_due():
    return total_amount_requested() - total_amount_paid()
