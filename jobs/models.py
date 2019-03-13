from django.db import models
from django.db.models import CASCADE, CharField, ForeignKey, TextField, DecimalField, Model, IntegerField, DateField
from django_extensions.db.models import TimeStampedModel


class Profession(Model):
    code = CharField(max_length=16)
    name = CharField(max_length=1024)
    addition = CharField(max_length=1024)


class Company(Model):
    name = CharField(max_length=1024)
    ic = CharField(max_length=16)


class Contact(Model):
    title = CharField(max_length=64, blank=True)
    first_name = CharField(max_length=256, blank=True)
    last_name = CharField(max_length=256)
    phone = CharField(max_length=64)
    email = CharField(max_length=256)
    address = CharField(max_length=1024, blank=True)


class Workplace(Model):
    address = TextField()


class Benefit(Model):
    code = CharField(max_length=16)
    name = CharField(max_length=256)
    description = CharField(max_length=1024)


class Skill(Model):
    code = CharField(max_length=16)
    name = CharField(max_length=256)


class Language(Model):
    code = CharField(max_length=16)
    name = CharField(max_length=256)
    level = models.CharField(max_length=64)


class Education(Model):
    code = CharField(max_length=16)
    name = CharField(max_length=256)


class Vacancy(TimeStampedModel):
    RELATED_NAME = 'vacancies'
    WAGE_TYPE_MONTHLY = 'Monthly'
    WAGE_TYPE_HOURLY = 'Hourly'
    SALARY_TYPES = (('M', WAGE_TYPE_MONTHLY), ('H', WAGE_TYPE_HOURLY))

    mpsv_id = IntegerField()
    profession = ForeignKey(to=Profession, on_delete=CASCADE) # PROFESE
    company = ForeignKey(to=Company, on_delete=CASCADE, null=True, related_name=RELATED_NAME)  # FIRMA
    workplace = ForeignKey(to=Workplace, on_delete=CASCADE, related_name=RELATED_NAME) # PRACOVISTE
    report_to = ForeignKey(to=Contact, on_delete=CASCADE, null=True, related_name=RELATED_NAME)  # KONOS
    salary_min = DecimalField(decimal_places=2, max_digits=8, null=True)  # MZDA
    salary_max = DecimalField(decimal_places=2, max_digits=8, null=True)
    salary_type = CharField(choices=SALARY_TYPES, null=True)
    appropriate_for = models.CharField()  # VHODNE_PRO
    comments = TextField(blank=True)  # POZNAMKA
    additional_information = CharField(max_length=1024)
    shift_rate = CharField(max_length=256)  # SMENNOST
    employment_period_from = DateField()  # PRAC_POMER
    employment_period_to = DateField()
    employment_relationship = CharField(max_length=256)  # PRACPRAVNI_VZTAH
    min_education = CharField(max_length=256)  # MIN_VZDELANI choices
    benefits = models.ManyToManyField(Benefit, related_name=RELATED_NAME)  # VYHODA
    skills = models.ManyToManyField(Skill, related_name=RELATED_NAME)  # DOVEDNOST
    languages = models.ManyToManyField(Language, related_name=RELATED_NAME)
    professions = models.ManyToManyField(Profession, related_name=RELATED_NAME)  # POVOLANI
    education = models.ManyToManyField(Education, related_name=RELATED_NAME)  # VZDELANI

