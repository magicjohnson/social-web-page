from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, CharField, DateField, OneToOneField, ForeignKey, IntegerField
from django_extensions.db.models import TimeStampedModel

User = get_user_model()

class WorkExperience(models.Model):
    LEVEL_CHOICES = (
        (1, 'Fundamental Awareness (basic knowledge)'),
        (2, 'Novice (limited experience)'),
        (3, 'Intermediate (practical application)'),
        (4, 'Advanced (applied theory)'),
        (5, 'Expert (recognized authority)'),
    )
    isco_08_code = CharField(max_length=16)
    experience_level = IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return '%s: %s (%s)' % (str(self.experience_level), self.isco_08_code, self.id)


class JobSeekerProfile(TimeStampedModel):
    user = OneToOneField(to=User, on_delete=CASCADE)
    first_name = CharField(max_length=256)
    last_name = CharField(max_length=256)
    city = ForeignKey(to='cities_light.City', on_delete=CASCADE)
    address1 = CharField(max_length=1024)
    address2 = CharField(max_length=1024, blank=True)
    citizenship = ForeignKey(to='cities_light.Country', on_delete=CASCADE)
    postal_code = CharField(max_length=64)
    contact_email = CharField(max_length=256)
    birthday = DateField()
    work_experience = models.ManyToManyField(to=WorkExperience, blank=True)

    def __str__(self):
        return '[%s] %s %s (%s)' % (self.user_id, self.first_name, self.last_name, self.id)

