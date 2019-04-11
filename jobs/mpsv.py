import logging
from xml.etree import ElementTree

from datetime import datetime

import pytz
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class MPSVParser(object):
    def __init__(self, xml):
        self.xml = xml
        self.namespace = '{http://portal.mpsv.cz/xml/exportvm}'
        self.updated_at = self.get_updated_at()

    def get_updated_at(self):
        tree = ElementTree.iterparse(self.xml, events=('start', ))
        for event, el in tree:
            tag = el.tag.lstrip(self.namespace)
            if tag == 'VOLNAMISTA':
                updated_timestamp = el.attrib.get('aktualizace')
                return pytz.utc.localize(datetime.strptime(updated_timestamp, '%Y-%m-%dT%H:%M:%S'))

    def iterate_vacancies(self):
        tree = ElementTree.iterparse(self.xml, events=('start', 'end'))
        data = {}
        for event, el in tree:
            tag = el.tag.lstrip(self.namespace)
            if tag == 'VOLNEMISTO':
                if event == 'start':
                    data = {tag: el}
                if event == 'end':
                    yield VacancyParser(data, self.updated_at).parse()
                continue
            if event == 'start':
                data[tag] = el


class VacancyParser(object):
    def __init__(self, data, updated_at=None):
        self.data = data
        self.vacancy = data['VOLNEMISTO']
        self.updated_at = updated_at
        self.namespaces = {'vm': 'http://portal.mpsv.cz/xml/exportvm'}

    def parse(self):
        uid = self.vacancy.attrib['uid']
        logger.debug(f'Parsing vacancy {uid}')
        data = {
            'uid': uid,
            'total_vacancies': int(self.vacancy.attrib['celkemVm']),
            'address': self.address,
            'region_codes': self.region_codes,
            'profession': self.profession,
            'employment_period_from': self.employment_period['from'],
            'is_for_foreign_workers': self.is_for_foreign_workers,
            'is_full_time': self.is_full_time,
            'updated_at': self.updated_at
        }
        optional_data = {
            'comments': self.comments,
            'town': self.town,
            'company': self.company,
            'report_to': self.report_to,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'employment_period_to': self.employment_period.get('to'),
        }
        data.update({k: v for k, v in optional_data.items() if v})
        return data

    @property
    def company(self):
        el = self.data.get('FIRMA')
        if hasattr(el, 'attrib'):
            return self.get_attrs(el, {'name': 'nazev'}, {'ic': 'ic'})

    @property
    def address(self):
        el = self.data.get('PRACOVISTE')
        return el.text

    @property
    def town(self):
        el = self.data.get('PRACOVISTE')
        return el.attrib.get('obec')

    @property
    def region_codes(self):
        el = self.data.get('PRACOVISTE')
        if 'okresKod' in el.attrib:
            return [el.attrib['okresKod']]

        if 'seznamOkresuKod' in el.attrib:
            return el.attrib['seznamOkresuKod'].split(',')
        return []

    @property
    def profession(self):
        el = self.data.get('PROFESE')
        return self.get_attrs(
            el,
            {'code': 'kod', 'name': 'nazev'},
            {'addition': 'doplnek'}
        )

    @property
    def report_to(self):
        el = self.data.get('KONOS')
        if hasattr(el, 'attrib'):
            return self.get_attrs(
                el,
                {'last_name': 'prijmeni'},
                {
                    'title': 'titul',
                    'first_name': 'jmeno',
                    'phone': 'telefon',
                    'email': 'email',
                }
            )

    @cached_property
    def employment_period(self):
        el = self.data.get('PRAC_POMER')
        result = {
            'from': datetime.strptime(el.attrib['od'], '%Y-%m-%d').date(),
        }
        if 'do' in el.attrib:
            result['to'] = datetime.strptime(el.attrib['do'], '%Y-%m-%d').date()
        return result

    @property
    def comments(self):
        el = self.data.get('POZNAMKA')
        if hasattr(el, 'text'):
            return el.text

    @property
    def salary_min(self):
        el = self.data.get('MZDA')
        if hasattr(el, 'attrib'):
            return el.attrib['min']

    @property
    def salary_max(self):
        el = self.data.get('MZDA')
        if hasattr(el, 'attrib'):
            return el.attrib.get('max')

    @property
    def is_full_time(self):
        el = self.data.get('PRACPRAVNI_VZTAH')
        return el.attrib['ppvztahPpPlny'] == 'A'

    @property
    def is_for_foreign_workers(self):
        el = self.data.get('VHODNE_PRO')
        return el.attrib['cizince'] == 'A'

    def get_attrs(self, element, required_attr_map, attr_map=None):
        data = {attr: element.attrib[xml_attr] for attr, xml_attr in required_attr_map.items()}
        if not attr_map:
            return data

        for attr, xml_attr in attr_map.items():
            if xml_attr in element.attrib:
                data[attr] = element.attrib[xml_attr]

        return data
