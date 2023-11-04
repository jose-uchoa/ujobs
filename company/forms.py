from django import forms

from .models import Company, Job


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_introduction"]

    def __init__(self, *args, **kwargs):
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Digite o nome da sua empresa."
        self.fields["company_introduction"].label = "Apresente sua empresa."


class CompanyJobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "location",
            "education",
            "hiring_type",
            "experience",
            "salary",
            "skills_required",
            "benefits",
            "job_description",
        ]

    # Defina mapeamento de campos para placeholders e rótulos
    field_info = {
        "title": {
            "placeholder": "Informe o título da vaga",
            "label": "Título da vaga",
        },
        "location": {
            "placeholder": "Informe o local da vaga",
            "label": "Local da vaga",
        },
        "education": {
            "label": "Escolaridade",
        },
        "hiring_type": {
            "placeholder": "Informe o tipo de vaga",
            "label": "Tipo de vaga",
        },
        "experience": {
            "placeholder": "Informe a experiência necessária",
            "label": "Experiência",
        },
        "salary": {
            "placeholder": "Informe a faixa salarial",
            "label": "Faixa salarial",
        },
        "skills_required": {
            "placeholder": "Informe as habilidades necessárias",
            "label": "Habilidades necessárias",
        },
        "benefits": {
            "placeholder": "Informe os benefícios",
            "label": "Benefícios",
        },
        "job_description": {
            "placeholder": "Descreva as atividades da vaga",
            "label": "Descrição das atividades",
        },
    }

    def __init__(self, *args, **kwargs):
        super(CompanyJobCreationForm, self).__init__(*args, **kwargs)

        # Configure placeholders e rótulos usando o mapeamento definido
        for field_name, field_attrs in self.field_info.items():
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs["id"] = "select-style"
                for attr_name, attr_value in field_attrs.items():
                    if attr_name == "placeholder":
                        field.widget.attrs[attr_name] = attr_value
                    else:
                        setattr(field, attr_name, attr_value)
