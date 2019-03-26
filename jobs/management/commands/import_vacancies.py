import argparse
import logging
import sys
import zipfile
from datetime import timedelta

import os

import requests
from django.core.management import BaseCommand
from django.db.transaction import atomic
from django.utils.timezone import now

from jobs.models import Profession, Vacancy, Company
from jobs.mpsv import MPSVParser
from social_web_page import settings

logger = logging.getLogger(__name__)


def tmp_path(*args):
    return os.path.join(settings.BASE_DIR, 'tmp', *args)

class Command(BaseCommand):
    help = "Import vacancies from MPSV portal XML file"

    def add_arguments(self, parser):
        parser.add_argument('--input_file', required=False, type=argparse.FileType(), help="a XML file that is used for import")
        parser.add_argument('--download', required=False, type=str, help="User `latest` word or specific filename to download vacancies file from https://portal.mpsv.cz", )

    def handle(self, *args, **options):
        downloaded_xml = None
        if options.get('download'):
            filename = self.get_filename(options)
            self.download(filename)
            downloaded_xml = self.unzip(filename)
        input_file = options['input_file'] or downloaded_xml
        logger.info(f'Parsing file {input_file}')
        parser = MPSVParser(input_file)
        success = 0
        for vacancy_data in parser.iterate_vacancies():
            self.create_or_update_vacancy(vacancy_data)
            success += 1

        sys.stdout.write('Successfully imported %d vacancies\n' % success)

    def get_filename(self, options):
        if options['download'] == 'latest':
            yesterday = now() - timedelta(days=1)
            return yesterday.strftime('vm%Y%m%d_xml.zip')
        return options['download']

    def download(self, filename):
        save_as = tmp_path(filename)
        if os.path.exists(save_as):
            logger.warning(f'File {save_as} already exists')
            return
        url = f'https://portal.mpsv.cz/portalssz/download/getfile.do?filename={filename}&_lang=cs_CZ'
        logger.info(f'Downloading from {url}')
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()

        logger.info(f'Saving file as: {save_as}')
        open(save_as, 'wb').write(response.content)

    def unzip(self, filename):
        xml_filename = filename.rstrip('_xml.zip') + '.xml'
        extract_dir = tmp_path(f'{filename}_extracted')
        path = os.path.join(extract_dir, xml_filename)
        if os.path.exists(path):
            return path

        with zipfile.ZipFile(tmp_path(filename)) as zip_file:
            logger.info(f'unzipping {filename} to {extract_dir}')
            zip_file.extractall(extract_dir, )

        if os.path.exists(path):
            return path

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
            logger.debug(f"Created new vacancy: {vacancy}")
        else:
            # TODO UPDATE Vacancy here
            pass
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
