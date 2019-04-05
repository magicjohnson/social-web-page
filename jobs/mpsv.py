from xml.etree import ElementTree

from datetime import datetime
from django.utils.functional import cached_property


class MPSVParser(object):
    def __init__(self, xml):
        self.xml = xml
        self.tree = ElementTree.parse(xml)
        self.root = self.tree.getroot()
        self.updated_at = datetime.strptime(self.root.attrib.get('aktualizace'), '%Y-%m-%dT%H:%M:%S')

    def iterate_vacancies(self):
        for vacancy_element in self.root:
            yield VacancyParser(vacancy_element, self.updated_at).parse()


class VacancyParser(object):
    def __init__(self, vacancy_tree, updated_at=None):
        self.vacancy = vacancy_tree
        self.updated_at = updated_at
        self.namespaces = {'vm': 'http://portal.mpsv.cz/xml/exportvm'}

    def parse(self):
        data = {
            'uid': self.vacancy.attrib['uid'],
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
        el = self.find('FIRMA')
        if el:
            return self.get_attrs(el, {'name': 'nazev', 'ic': 'ic'})

    @property
    def address(self):
        el = self.find('PRACOVISTE')
        return el.text

    @property
    def town(self):
        el = self.find('PRACOVISTE')
        return el.attrib.get('obec')

    @property
    def region_codes(self):
        el = self.find('PRACOVISTE')
        if 'okresKod' in el.attrib:
            return [el.attrib['okresKod']]

        return el.attrib['seznamOkresuKod'].split(',')

    @property
    def profession(self):
        el = self.find('PROFESE')
        return self.get_attrs(
            el,
            {'code': 'kod', 'name': 'nazev'},
            {'addition': 'doplnek'}
        )

    @property
    def report_to(self):
        el = self.find('KONOS')
        if el:
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
        el = self.find('PRAC_POMER')
        result = {
            'from': datetime.strptime(el.attrib['od'], '%Y-%m-%d').date(),
        }
        if 'do' in el.attrib:
            result['to'] = datetime.strptime(el.attrib['do'], '%Y-%m-%d').date()
        return result

    @property
    def comments(self):
        el = self.find('POZNAMKA')
        if hasattr(el, 'text'):
            return el.text

    @property
    def salary_min(self):
        el = self.find('MZDA')
        if el:
            return el.attrib['min']

    @property
    def salary_max(self):
        el = self.find('MZDA')
        if el:
            return el.attrib['max'],

    @property
    def is_full_time(self):
        el = self.find('PRACPRAVNI_VZTAH')
        return el.attrib['ppvztahPpPlny'] == 'A'

    @property
    def is_for_foreign_workers(self):
        el = self.find('VHODNE_PRO')
        return el.attrib['cizince'] == 'A'

    def find(self, tag):
        return self.vacancy.find('vm:%s' % tag, self.namespaces)

    def get_attrs(self, element, required_attr_map, attr_map=None):
        data = {attr: element.attrib[xml_attr] for attr, xml_attr in required_attr_map.items()}
        if not attr_map:
            return data

        for attr, xml_attr in attr_map.items():
            if xml_attr in element.attrib:
                data[attr] = element.attrib[xml_attr]

        return data
