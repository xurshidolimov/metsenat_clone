from django.db import models


class CustomManager(models.Manager):
    def get_student(self, id):
        return super().get_queryset().get(id=id)

    def get_sponsor(self, id):
        return super().get_queryset().get(id=id)
