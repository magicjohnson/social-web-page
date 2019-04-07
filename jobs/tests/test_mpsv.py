from unittest import TestCase

import os

from datetime import date, datetime

from pytz import UTC

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
            'total_vacancies': 5,
            'region_codes': ['3703'],
            'town': 'Kuřim',
            'address': 'Prefa Brno a.s. - 01, Blanenská 1190/121, 664 34  Kuřim',
            'profession': {
                'code': '71140',
                'name': 'Betonáři, železobetonáři a příbuzní pracovníci',
            },
            'is_for_foreign_workers': True,
            'employment_period_from': date(2018, 12, 15),
            'is_full_time': True,
            'updated_at': datetime(2019, 2, 19, 1, 55, 41, tzinfo=UTC)
        }
        self.assertEqual(vacancy, expected)

    def test_parse_vacancy_with_optional_data__should_return_that_data(self):
        parser = MPSVParser(get_test_data('vacancy.xml'))
        vacancy = next(parser.iterate_vacancies())
        expected = {
            'uid': '13729580791',
            'total_vacancies': 1,
            'region_codes': [
                '3100', '3201', '3202', '3203', '3204', '3205', '3206', '3207', '3208', '3209', '3210', '3211', '3212', '3301', '3302', '3303',
                '3304', '3305', '3306', '3307', '3308', '3401', '3402', '3403', '3404', '3405', '3406', '3407', '3408', '3409', '3410', '3501',
                '3502', '3503', '3504', '3505', '3506', '3507', '3508', '3509', '3510', '3601', '3602', '3603', '3604', '3605', '3606', '3607',
                '3608', '3609', '3610', '3611', '3701', '3702', '3703', '3704', '3705', '3706', '3707', '3708', '3709', '3710', '3711', '3712',
                '3713', '3714', '3801', '3802', '3803', '3804', '3805', '3806', '3807', '3808', '3809', '3810', '3811'
            ],
            'company': {'ic': '25723944', 'name': 'Sconto Nábytek, s.r.o.'},
            'report_to': {'email': 'kariera@sconto.cz', 'last_name': 'Bc. Zdeněk Jásek'},
            'salary_max': '30000',
            'salary_min': '24000',
            'address': 'Sconto Nábytek, s.r.o. celá ČR, Benešov, Beroun, Blansko,\n'
            '      Brno-město, Brno-venkov, Bruntál, Břeclav, Česká Lípa, '
            'České Budějovice, Český Krumlov, Děčín, Domažlice,\n'
            '      Frýdek-Místek, Havlíčkův Brod, Hlavní město Praha, Hodonín, '
            'Hradec Králové, Cheb, Chomutov, Chrudim, Jablonec\n'
            '      nad\n'
            '      Niso...\n'
            '    ',
            'profession': {
                'code': '3432',
                'name': 'Aranžéři a příbuzní pracovníci',
                'addition': 'Dekoratéři obchodního domu pro Česko',
            },
            'comments': 'Místo výkonu práce: celá ČR\n'
             '      Kontakt: Bc. Zdeněk Jásek, e-mail: kariera@sconto.cz\n'
             '    ',
            'employment_period_from': date(2017, 12, 20),
            'is_for_foreign_workers': False,
            'is_full_time': True,
            'updated_at': datetime(2019, 3, 25, 1, 53, 16, tzinfo=UTC),
        }
        self.assertEqual(vacancy, expected)
