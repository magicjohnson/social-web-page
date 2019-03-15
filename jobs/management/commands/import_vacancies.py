import logging
import sys

from django.core.management import BaseCommand
from django.db.transaction import atomic

from jobs.models import Profession, Vacancy, Company
from jobs.mpsv import MPSVParser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import vacancies from MPSV portal XML file"

    def add_arguments(self, parser):
        parser.add_argument('input_file', )

    def handle(self, *args, **options):
        input_file = options['input_file']
        parser = MPSVParser(input_file)

        success = 0
        for vacancy_data in parser.iterate_vacancies():
            self.create_or_update_vacancy(vacancy_data)
            success += 1

        sys.stdout.write('Successfully imported %d vacancies\n' % success)

    @atomic
    def create_or_update_vacancy(self, vacancy_data):
        uid = vacancy_data['uid']
        defaults = {
            'profession': self.get_or_create_profession(vacancy_data),
            'company': self.get_or_create_company(vacancy_data),
            'employment_period_from': vacancy_data['employment_period_from'],
            'is_full_time': vacancy_data['is_full_time'],
            'employment_period_to': vacancy_data.get('employment_period_to'),

        }
        vacancy, created = Vacancy.objects.get_or_create(mpsv_id=uid, defaults=defaults)
        if created:
            logger.debug("Created new vacancy: %s" % vacancy)
        else:
            print(uid)
        return vacancy

    def get_or_create_company(self, vacancy_data):
        if 'company' not in vacancy_data:
            return
        company_data = vacancy_data['company']
        company, created = Company.objects.get_or_create(ic=company_data['ic'], defaults={'name': company_data['name']})
        if created:
            logger.debug('created new company: %s' % company)
        return company

    def get_or_create_profession(self, vacancy_data):
        profession = vacancy_data['profession']
        profession, created = Profession.objects.get_or_create(code=profession['code'], defaults={'name': profession['name'], 'addition': profession.get('addition', '')})
        if created:
            logger.debug('created new profession: %s' % profession)
        return profession
