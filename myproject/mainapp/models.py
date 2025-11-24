from django.db import models


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True,
    verbose_name='Название')
class Meta:
    verbose_name_plural = 'Рубрики'
    verbose_name = 'Рубрика'
    ordering = ['name'] 