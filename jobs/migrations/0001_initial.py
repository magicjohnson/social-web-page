# Generated by Django 2.2 on 2019-04-07 07:31

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ic', models.CharField(max_length=16, null=True)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64)),
                ('first_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=256)),
                ('address', models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('level', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=1024)),
                ('addition', models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('mpsv_id', models.BigIntegerField(unique=True)),
                ('mpsv_updated_at', models.DateTimeField()),
                ('total_vacancies', models.IntegerField()),
                ('town', models.CharField(blank=True, max_length=256)),
                ('address', models.CharField(max_length=1024)),
                ('salary_min', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('salary_max', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('salary_type', models.CharField(choices=[('M', 'Monthly'), ('H', 'Hourly')], max_length=16, null=True)),
                ('is_for_foreign_workers', models.BooleanField()),
                ('comments', models.TextField(blank=True)),
                ('shift_rate', models.CharField(max_length=256)),
                ('employment_period_from', models.DateField()),
                ('employment_period_to', models.DateField(null=True)),
                ('is_full_time', models.BooleanField()),
                ('min_amount_of_hours', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('min_education', models.CharField(max_length=256)),
                ('benefits', models.ManyToManyField(related_name='vacancies', to='jobs.Benefit')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobs.Company')),
                ('education', models.ManyToManyField(related_name='vacancies', to='jobs.Education')),
                ('languages', models.ManyToManyField(related_name='vacancies', to='jobs.Language')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Profession')),
                ('professions', models.ManyToManyField(related_name='vacancies', to='jobs.Profession')),
                ('region_codes', models.ManyToManyField(to='jobs.Region')),
                ('report_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobs.Contact')),
                ('skills', models.ManyToManyField(related_name='vacancies', to='jobs.Skill')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
