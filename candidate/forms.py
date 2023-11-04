from django import forms
from core.models import User

from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]

    def __init__(self, *args, **kwargs):
        super(CandidateProfileForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].label = "Nome Completo "
        self.fields["email"].label = "E-mail "


class CandidateResumeForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ["resume"]

    def __init__(self, *args, **kwargs):
        super(CandidateResumeForm, self).__init__(*args, **kwargs)
        self.fields["resume"].label = "Currículo (arquivo)"
        self.fields["resume"].help_text = "Envie seu currículo em formato PDF"
