from admin_numeric_filter.admin import SliderNumericFilter, NumericFilterModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filter import DateRangeFilter

from jobs import models


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 0
    STEP = 10

@admin.register(models.Vacancy)
class VacancyAdmin(NumericFilterModelAdmin):
    list_display = (
        'mpsv_id',
        'total_vacancies',
        'profession',
        'get_contact',
        'employment_period_to',
        'get_salary',
        'is_for_foreign_workers',
        'mpsv_updated_at',
        'get_region_codes',
        'town',
    )

    search_fields = (
        'mpsv_id',
        'region_codes__code',
        'profession__code',
    )

    list_filter = (
        ('salary_min', CustomSliderNumericFilter),
        ('salary_max', CustomSliderNumericFilter),
        ('employment_period_to', DateRangeFilter),
        'is_for_foreign_workers',
    )

    def get_region_codes(self, obj):
        codes = [r.code for r in obj.region_codes.all()[:5]]
        truncate_char = '...' if len(codes) > 5 else ''
        return '\n'.join(codes) + truncate_char

    get_region_codes.short_description = 'Region codes'

    def get_contact(self, obj):
        if not obj.report_to:
            return
        return format_html('{}<br> {}', obj.report_to.email, obj.report_to.phone)

    get_contact.short_description = 'Email, phone'

    def get_salary(self, obj):
        salary_min_str = '%.0d' % obj.salary_min if obj.salary_min else '...'
        salary_max_str = '%.0d' % obj.salary_max if obj.salary_max else '...'

        return '%s - %s' % (salary_min_str, salary_max_str)

    get_salary.short_description = 'min/max salary'
