from xml.etree import ElementTree

from datetime import datetime
from django.utils.functional import cached_property


class MPSVParser(object):
    def __init__(self, xml):
        self.xml = xml
        self.tree = ElementTree.parse(xml)
        self.root = self.tree.getroot()

    def iterate_vacancies(self):
        for vacancy_element in self.root:
            yield VacancyParser(vacancy_element).parse()


class VacancyParser(object):
    def __init__(self, vacancy_tree):
        self.vacancy = vacancy_tree
        self.namespaces = {'vm': 'http://portal.mpsv.cz/xml/exportvm'}

    def parse(self):
        data = {
            'uid': self.vacancy.attrib.get('uid'),
            'address': self.address,
            'profession': self.profession,
            'employment_period_from': self.employment_period['from'],
            'is_full_time': self.is_full_time,
        }
        optional_data = {
            'company': self.company,
            'report_to': self.report_to,
            'employment_period_to': self.employment_period.get('to'),
        }
        data.update({k:v for k, v in optional_data.items() if v})
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
        if el:
            return el.text

    @property
    def is_full_time(self):
        el = self.find('PRACPRAVNI_VZTAH')
        return el.attrib['ppvztahPpPlny'] == 'A'

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
