from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Sponsor, Student, Metsenat
from users.serializers import SponsorSerializer, StudentSerializer, SponsorRegisterSerializer, MetsenatSerializer
from .pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter
from .filters import CustomFilter
from .permissions import CustomPermissions
from .utility import sponsors_by_month, students_by_month, total_amount_paid, total_amount_requested, amount_due


class SponsorRegisterView(APIView):
    def post(self, request):
        serializer = SponsorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Ma'lumot tekshirish uchun yuborildi"}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = [CustomPermissions]

    def get(self, request):
        return Response(data={
            "total_amount_paid": total_amount_paid(),
            "total_amount_requested": total_amount_requested(),
            "amount_due": amount_due(),
            "students_by_month": students_by_month(),
            "sponsor_by_month": sponsors_by_month(),
        })


class SponsorViewSet(viewsets.ReadOnlyModelViewSet, viewsets.mixins.UpdateModelMixin):
    permission_classes = [CustomPermissions]
    queryset = Sponsor.manager.all()
    serializer_class = SponsorSerializer
    lookup_field = 'id'
    pagination_class = MyPageNumberPagination
    filter_backends = (CustomFilter, SearchFilter)
    filterset_fields = ('payment_amount', 'status', 'created_at')
    search_fields = ('full_name',)


class StudentsView(generics.ListCreateAPIView):
    permission_classes = [CustomPermissions]
    queryset = Student.manager.all()
    serializer_class = StudentSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('degree_type', 'university_name')
    search_fields = ('full_name',)


class MetsenatView(APIView):
    permission_classes = [CustomPermissions]

    def get(self, request, student_id):
        student = Student.manager.get_student(student_id)
        student_serializer = StudentSerializer(student)

        metsenat = Metsenat.objects.filter(student_id=student_id)
        serializer = MetsenatSerializer(metsenat, many=True)

        return Response(data={
            "student": student_serializer.data,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        serializer = MetsenatSerializer(data=request.data)
        if serializer.is_valid():
            Metsenat.objects.bulk_create([
                Metsenat(
                    sponsor_id=request.data['sponsor_id'],
                    student_id=student_id,
                    money=request.data['money'],
                ),
            ])
            return Response(data={"message": "Successful"}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, student_id):
        student = Student.manager.get_student(student_id)
        serializer = StudentSerializer(instance=student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
