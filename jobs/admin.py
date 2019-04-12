from admin_numeric_filter.admin import NumericFilterModelAdmin
from admin_numeric_filter.forms import SingleNumericForm
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field
from rangefilter.filter import DateRangeFilter

from jobs import models


class StartsWithNumericFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = 'admin/filter_numeric_single.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        self.request = request

        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def expected_parameters(self):
        return [self.parameter_name]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{'%s__startswith' % self.parameter_name: self.value()})

    def value(self):
        return self.used_parameters.get(self.parameter_name, None)

    def choices(self, changelist):
        return ({
            'request': self.request,
            'parameter_name': self.parameter_name,
            'form': SingleNumericForm(name=self.parameter_name, data={self.parameter_name: self.value()}),
        }, )


class VacancyResource(resources.ModelResource):
    region_codes = Field()

    class Meta:
        model = models.Vacancy
        fields = (
            'mpsv_id',
            'total_vacancies',
            'profession__code',
            'profession__name',
            'report_to__email',
            'report_to__phone',
            'employment_period_to',
            'salary_min',
            'salary_max',
            'is_for_foreign_workers',
            'mpsv_updated_at',
            'region_codes',
            'town',
        )

    def dehydrate_region_codes(self, obj):
        return ' '.join(r.code for r in obj.region_codes.all())


@admin.register(models.Vacancy)
class VacancyAdmin(ExportMixin, NumericFilterModelAdmin):
    resource_class = VacancyResource

    fields = (
        'comments',
    )

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
        'profession__name',
        'comments',
    )

    list_filter = (
        ('profession__code', StartsWithNumericFilter),
        ('employment_period_to', DateRangeFilter),
        'is_for_foreign_workers',
    )

    def get_region_codes(self, obj):
        codes = [r.code for r in obj.region_codes.all()[:10]]
        truncate_char = ' ...' if len(codes) == 10 else ''
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
