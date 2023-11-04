from django.utils import timezone
from django.db import models
from core.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Company(models.Model):
    company = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    company_introduction = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)


class Job(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    title = models.CharField(max_length=80)
    location = models.CharField(max_length=80)

    created_date = models.DateTimeField(default=timezone.now, blank=True)

    experience_choices = (
        ("no_matter", "Não importa"),
        ("1_to_3", "De 1 a 3 anos"),
        ("3_to_6", "De 3 a 6 anos"),
        ("above_6", "Acima de 6 anos"),
    )
    experience = models.CharField(max_length=80, choices=experience_choices)

    salary_choices = (
        ("agreement", "A combinar"),
        ("up_to_1000", "Até 1.000"),
        ("from_1000_to_2000", "De 1.000 a 2.000"),
        ("from_2000_to_3000", "De 2.000 a 3.000"),
        ("above_3000", "Acima de 3.000"),
    )
    salary = models.CharField(max_length=80, choices=salary_choices)

    hiring_choices = (
        ("full_time", "Período integral"),
        ("part_time", "Meio período"),
        ("remote", "Trabalho remoto"),
        ("internship", "Estágio"),
    )
    hiring_type = models.CharField(
        max_length=80,
        choices=hiring_choices,
    )

    job_description = models.TextField()
    skills_required = models.CharField(max_length=120)
    benefits = models.CharField(max_length=120)

    education_choices = (
        ("no_matter", "Não importa"),
        ("elementary_school", "Ensino Fundamental"),
        ("high_school", "Ensino Médio"),
        ("technical_degree", "Tecnólogo"),
        ("undergraduate", "Ensino Superior"),
        ("postgraduate", "Pós / MBA / Mestrado"),
        ("doctorate", "Doutorado"),
    )

    education = models.CharField(max_length=80, choices=education_choices)

    # Campo para armazenar o slug
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title


# Função para gerar um slug automaticamente
@receiver(pre_save, sender=Job)
def pre_save_job(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class JobRequests(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume_url = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    hired = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=80, default="Pendente")

    def __str__(self):
        return f"{self.candidate} requested on {self.job}"

    def save(self, *args, **kwargs):
        super(JobRequests, self).save(*args, **kwargs)
