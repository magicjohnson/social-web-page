from django.db import models
from django.db.models import CASCADE, CharField, ForeignKey, TextField, DecimalField, Model, IntegerField, DateField
from django_extensions.db.models import TimeStampedModel


class Profession(models.Model):
    code = CharField(max_length=16, unique=True)
    name = CharField(max_length=1024)
    addition = CharField(max_length=1024, blank=True)

    def __str__(self):
        return '%s: %s' % (self.code, self.name)

class Company(Model):
    ic = CharField(max_length=16, unique=True)
    name = CharField(max_length=1024)

    def __str__(self):
        return '%s: %s' % (self.ic, self.name)


class Contact(Model):
    title = CharField(max_length=64, blank=True)
    first_name = CharField(max_length=256, blank=True)
    last_name = CharField(max_length=256)
    phone = CharField(max_length=64)
    email = CharField(max_length=256)
    address = CharField(max_length=1024, blank=True)


class Benefit(Model):
    code = CharField(max_length=16, unique=True)
    name = CharField(max_length=256)
    description = CharField(max_length=1024)


class Skill(Model):
    code = CharField(max_length=16, unique=True)
    name = CharField(max_length=256)


class Language(Model):
    code = CharField(max_length=16, unique=True)
    name = CharField(max_length=256)
    level = models.CharField(max_length=64)


class Education(Model):
    code = CharField(max_length=16, unique=True)
    name = CharField(max_length=256)


class Vacancy(TimeStampedModel):
    RELATED_NAME = 'vacancies'
    WAGE_TYPE_MONTHLY = 'Monthly'
    WAGE_TYPE_HOURLY = 'Hourly'
    SALARY_TYPES = (('M', WAGE_TYPE_MONTHLY), ('H', WAGE_TYPE_HOURLY))

    mpsv_id = IntegerField(unique=True)
    profession = ForeignKey(to=Profession, on_delete=CASCADE)  # PROFESE
    company = ForeignKey(to=Company, on_delete=CASCADE, null=True, related_name=RELATED_NAME)  # FIRMA
    address = CharField(max_length=1024)  # PRACOVISTE
    report_to = ForeignKey(to=Contact, on_delete=CASCADE, null=True, related_name=RELATED_NAME)  # KONOS
    salary_min = DecimalField(decimal_places=2, max_digits=8, null=True)  # MZDA
    salary_max = DecimalField(decimal_places=2, max_digits=8, null=True)
    salary_type = CharField(choices=SALARY_TYPES, max_length=16, null=True)
    # appropriate_for = models.CharField(max_length=512)  # VHODNE_PRO
    comments = TextField(blank=True)  # POZNAMKA
    shift_rate = CharField(max_length=256)  # SMENNOST
    employment_period_from = DateField()  # PRAC_POMER
    employment_period_to = DateField(null=True)
    is_full_time = models.BooleanField() # PRACPRAVNI_VZTAH ppvztahPpPlny / ppvztahPpZkrac
    min_amount_of_hours = models.DecimalField(decimal_places=2, max_digits=5, null=True) # tydneHodinMin
    min_education = CharField(max_length=256)  # MIN_VZDELANI choices
    benefits = models.ManyToManyField(Benefit, related_name=RELATED_NAME)  # VYHODA
    skills = models.ManyToManyField(Skill, related_name=RELATED_NAME)  # DOVEDNOST
    languages = models.ManyToManyField(Language, related_name=RELATED_NAME)
    professions = models.ManyToManyField(Profession, related_name=RELATED_NAME)  # POVOLANI
    education = models.ManyToManyField(Education, related_name=RELATED_NAME)  # VZDELANI

    def __str__(self):
        return '%s' % self.mpsv_id
