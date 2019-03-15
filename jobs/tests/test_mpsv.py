from unittest import TestCase

import os

from datetime import date

from jobs.mpsv import MPSVParser


def get_test_data(filename):
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, 'data', filename)


class MPSVParserTest(TestCase):
    def test_iterate_vacancies__when_no_vacancies__should_return_none(self):
        parser = MPSVParser(get_test_data('no_vacancies.xml'))
        self.assertEqual(0, len(list(parser.iterate_vacancies())))

    def test_iterate_vacancies__should_return_iterator(self):
        parser = MPSVParser(get_test_data('vacancies.xml'))
        self.assertEqual(10, len(list(parser.iterate_vacancies())))

    def test_parse_vacancy__should_return_vacancy_data(self):
        parser = MPSVParser(get_test_data('vacancy_required_data_only.xml'))
        vacancy = next(parser.iterate_vacancies())
        expected = {
            'uid': '14918890710',
            'address': 'Prefa Brno a.s. - 01, Blanenská 1190/121, 664 34  Kuřim',
            'profession': {
                'code': '71140',
                'name': 'Betonáři, železobetonáři a příbuzní pracovníci',
            },
            'employment_period_from': date(2018, 12, 15),
            'is_full_time': True,
        }
        self.assertEqual(vacancy, expected)
