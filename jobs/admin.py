from django.contrib import admin

from jobs import models


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mpsv_id', 'profession', 'company', 'created', 'modified')


