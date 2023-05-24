from django.core.validators import RegexValidator
from django.db import models
from .manager import CustomManager
from django.contrib.auth.password_validation import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from telegram.signals import add_sponsor, edit_sponsor, add_student, edit_student


class BaseModel(models.Model):
    _validate_phone = RegexValidator(
        regex=r"^998[0-9]{9}$",
        message="Telefon raqamingiz 9 bilan boshlanishi va 12 ta belgidan oshmasligi lozim. Masalan: 998993451545",
    )
    full_name = models.CharField(max_length=64, verbose_name='F.I.SH', unique=True)
    phone_number = models.CharField(max_length=12, validators=[_validate_phone], verbose_name='Telefon nomer')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sana')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Oxirgi yangilanish vaqti')

    class Meta:
        abstract = True


class Sponsor(BaseModel):
    SPONSOR_TYPE = (
        ("PHYSICAL_PERSON", 'Jismoniy shaxs'),
        ("LEGAL_ENTITY", 'Yuridik shaxs')
    )
    PAYMENT_TYPE = (
        ("VIA_CASH", 'Naqd pul'),
        ("VIA_CARD", 'Plastik karta'),
        ("VIA_BANK", 'Bank hisobi')
    )
    STATUS = (
        ("NEW", 'Yangi'),
        ("IN_MODERNIZATION", 'Modernizatsiyada'),
        ("APPROVED", 'Tasdiqlangan'),
        ("CANCELLED", 'Bekor qilingan')
    )
    sponsor_type = models.CharField(max_length=31, choices=SPONSOR_TYPE,
                                    default="PHYSICAL_PERSON", verbose_name='Homiy turi')
    organization_name = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name='Tashkilot nomi')
    status = models.CharField(max_length=31, choices=STATUS, default="NEW",
                                    verbose_name='Holati')
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPE, null=True,
                                    blank=True, verbose_name="To'lov turi")
    payment_amount = models.PositiveIntegerField(verbose_name='Homiylik summasi')
    amount_spent = models.PositiveIntegerField(default=0, verbose_name='Sarflangan summa')

    REQUIRED_FIELDS = ["full_name", "phone_number", "sponsor_type", "payment_amount"]
    manager = CustomManager()

    def __str__(self):
        return self.full_name

    @property
    def about_sponsor(self):
        return f"{self.full_name}. " \
               f"\nTelefon raqami: {self.phone_number}. " \
               f"\nHomiylik summasi: {self.payment_amount}. " \
               f"\nSarflandi: {self.amount_spent}"

    class Meta:
        ordering = ("created_at",)
        verbose_name_plural = "Homiylar"

    def clean(self):
        if self.sponsor_type == "LEGAL_ENTITY" and not self.organization_name:
            raise ValidationError(
                'Tashkilot nomini kiriting.'
            )

    def save(self, *args, **kwargs):
        if self.sponsor_type == "PHYSICAL_PERSON":
            self.organization_name = None
        super(Sponsor, self).save(*args, **kwargs)


@receiver(post_save, sender=Sponsor)
def post_save_sponsor(sender, instance, created, *args, **kwargs):
    if created:
        add_sponsor(instance)
    else:
        edit_sponsor(instance)


class Student(BaseModel):
    DEGREE_TYPE = (
        ("BACHELOR", 'Bakalavr'),
        ("MASTER", 'Magistr')
    )
    university_name = models.CharField(max_length=64, verbose_name='Unversitet nomi')
    degree_type = models.CharField(max_length=15, choices=DEGREE_TYPE, verbose_name='Talabalik turi')
    payment_amount = models.PositiveIntegerField(verbose_name='Kontrakt miqdori')
    amount_spent = models.PositiveIntegerField(default=0, verbose_name='Ajratilgan summa')

    REQUIRED_FIELDS = ["full_name", "phone_number", "university_name", "degree_type", "payment_amount"]
    manager = CustomManager()

    def __str__(self):
        return self.full_name

    @property
    def about_student(self):
        return f"{self.full_name}. " \
               f"\nTelefon raqami: {self.phone_number}. " \
               f"\nKontrakt summasi: {self.payment_amount}. " \
               f"\nAjratildi: {self.amount_spent}"

    class Meta:
        ordering = ("created_at",)
        verbose_name_plural = "Talabalar"


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, *args, **kwargs):
    if created:
        add_student(instance)
    else:
        edit_student(instance)


class Metsenat(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    money = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.full_name} >>> {self.student.full_name}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Metsenat"

    def clean(self):
        alfa = self.sponsor.payment_amount - self.sponsor.amount_spent
        betta = self.student.payment_amount - self.student.amount_spent
        if self.sponsor.status != "APPROVED":
            raise ValidationError(
                "Homiy tasdiqlanmagan"
            )
        if self.student.payment_amount == self.student.amount_spent:
            raise ValidationError(
                "Ushbu talaba uchun mablag' yetarli"
            )
        if self.sponsor.payment_amount == self.sponsor.amount_spent:
            raise ValidationError(
               "Homiyda mablag' qolmadi."
            )
        if self.money > alfa:
            raise ValidationError(
               f"Homiyda mablag' yetarli emas.\n"
               f"Homiyda {alfa} so'm qoldi"
            )
        if self.money > betta:
            raise ValidationError(
               f"Ushbu talaba uchun keragidan ortiq summa kiritdingiz.\n"
               f"Kerakli mablag' {betta}"
            )

    def save(self, *args, **kwargs):
        sponsor = Sponsor.manager.get_sponsor(self.sponsor.id)
        sponsor.amount_spent += self.money
        sponsor.save()

        student = Student.manager.get_student(self.student.id)
        student.amount_spent += self.money
        student.save()

        super(Metsenat, self).save(*args, **kwargs)






