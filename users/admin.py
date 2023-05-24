from django.contrib import admin
from .models import Sponsor, Student, Metsenat


class SponsorAdmin(admin.ModelAdmin):
    list_filter = ('sponsor_type', 'status', 'payment_type')
    search_fields = ['full_name']
    list_display_links = ('full_name',)
    list_display = ('id', 'full_name', 'phone_number', 'payment_amount', 'amount_spent', 'created_at', 'status')


class StudentAdmin(admin.ModelAdmin):
    list_filter = ('degree_type',)
    search_fields = ['full_name']
    list_display_links = ('full_name',)
    list_display = ('id', 'full_name', 'university_name', 'payment_amount', 'amount_spent')


class MetsenatAdmin(admin.ModelAdmin):
    # search_fields = ('student', 'sponsor')
    list_display_links = ('student',)
    list_display = ('id', 'student', 'sponsor', 'money')


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Metsenat, MetsenatAdmin)
