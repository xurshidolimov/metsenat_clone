from django.urls import path, include
from .views import StudentsView, SponsorRegisterView, DashboardView, MetsenatView


urlpatterns = [
    path('sponsor_register/', SponsorRegisterView.as_view()),
    path('', DashboardView.as_view()),
    path('sponsor/', include('users.routers')),
    path('students/', StudentsView.as_view()),
    path('metsenat/<int:student_id>/', MetsenatView.as_view()),
]
