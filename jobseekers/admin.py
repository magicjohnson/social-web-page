from django.contrib import admin

from jobseekers import models


@admin.register(models.WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    pass


class WorkExperienceInline(admin.TabularInline):
    model = models.JobSeekerProfile.work_experience.through


@admin.register(models.JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'first_name', 'last_name', 'created', 'modified')
    inlines = [
        WorkExperienceInline,
    ]
