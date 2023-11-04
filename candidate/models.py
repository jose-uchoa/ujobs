from django.db import models

from company.models import Job
from core.models import User


class CandidateProfile(models.Model):
    candidate = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    resume = models.FileField(null=True, upload_to="user_resume")

    def __str__(self):
        return f"Perfil de {self.candidate}"


class CandidateRequests(models.Model):
    requests = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=80, default="Em análise")

    def __str__(self):
        return f"Solicitação de {self.requests} para {self.job}"

    def save(self, *args, **kwargs):
        super(CandidateRequests, self).save(*args, **kwargs)
