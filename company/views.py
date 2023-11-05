from datetime import datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import CompanyJobCreationForm, CompanyProfileForm
from .models import Company, JobRequests, Job


def is_company(user):
    try:
        if user.is_candidate:
            raise Http404
        return True
    except Http404:
        raise Http404


@user_passes_test(is_company)
@login_required
def company_home(request):
    try:
        requests = JobRequests.objects.filter(
            company=request.user.company, accepted=False
        ).all()
        accepted_requests = JobRequests.objects.filter(
            company=request.user.company, accepted=True
        ).all()
    except Company.DoesNotExist:
        messages.info(
            request,
            "Para acessar outras seções, \
                primeiro complete as informações abaixo",
        )
        return redirect("company-profile")
    context = {
        "requests": requests,
        "accepted_requests": accepted_requests,
    }
    return render(request, "company_home.html", context)


@user_passes_test(is_company)
@login_required
def company_profile(request):
    # Se o usuário já tiver um perfil, mostrar suas informações no formulário
    try:
        if request.method == "POST":
            form = CompanyProfileForm(
                request.POST, request.FILES, instance=request.user.company
            )
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = request.user
                instance.save()
                messages.success(
                    request,
                    "Seu perfil foi atualizado com sucesso.",
                )
                return redirect("company-profile")
        form = CompanyProfileForm(instance=request.user.company)
    except Company.DoesNotExist:
        # Se o usuário for novo e ainda não tiver um perfil
        if request.method == "POST":
            form = CompanyProfileForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = request.user
                instance.save()
                messages.success(request, "Seu perfil foi criado com sucesso.")
                messages.success(
                    request,
                    """
                        Para criar um anúncio, selecione a opção
                        'Novo Anúncio' no menu superior.
                        """,
                )
                return redirect("company-profile")
        form = CompanyProfileForm()
    return render(request, "profile.html", {"form": form})


@user_passes_test(is_company)
@login_required
def company_jobs(request):
    # Mostrar todos os empregos publicados pelo empregador/empresa.
    try:
        jobs = request.user.company.jobs.all()
        now = datetime.now(timezone.utc)
        for i in jobs:
            get_days = now - i.created_date
            if get_days.days > 1:
                i.created_date = f"{get_days.days} dias atrás"
        requests = JobRequests.objects.filter(company=request.user.company)
    except Company.DoesNotExist:
        return redirect("company-home")
    return render(
        request,
        "jobs.html",
        {"jobs": jobs, "number": len(requests)},
    )


@user_passes_test(is_company)
@login_required
def company_create_job(request):
    # Criar um emprego e publicá-lo no portal.
    try:
        if request.method == "POST":
            form = CompanyJobCreationForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = request.user.company
                instance.save()
                messages.success(request, "Seu anúncio foi publicado.")
                return redirect("job-detail", slug=instance.slug)
        elif request.method == "GET":
            form = CompanyJobCreationForm()
    except Company.DoesNotExist:
        raise Http404
    return render(request, "create_job.html", {"form": form})


@login_required
def company_update_job(request, slug):
    try:
        job = Job.objects.get(slug=slug, company=request.user.company)
    except Job.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = CompanyJobCreationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Seu anúncio foi atualizado.")
            return redirect("job-detail", slug=slug)
    elif request.method == "GET":
        form = CompanyJobCreationForm(instance=job)
    return render(request, "update_job.html", {"form": form})


@login_required
def company_delete_job(request, slug):
    try:
        job = Job.objects.get(slug=slug, company=request.user.company)
    except Job.DoesNotExist:
        raise Http404

    if request.method == "POST":
        job.delete()
        messages.success(request, "Seu anúncio foi excluído com sucesso.")
        return redirect("company-jobs")
    return render(request, "delete_confirm.html", {"job": job})


def accepted_status(request, slug):
    job_request = get_object_or_404(JobRequests, job__slug=slug)
    job_request.accepted = True
    job_request.status = "Aceito"  # Defina o status como 'Aceito'
    job_request.save()

    # Atualize também o status de aceitação na tabela de
    # solicitações de candidatos a emprego
    candidate_request = job_request.candidate.requests.filter(
        job__slug=slug,
    ).first()

    if candidate_request:
        candidate_request.status = "Aceito"
        candidate_request.save()

    messages.success(request, "Solicitação aceita com sucesso.")
    return redirect("company-home")


def reject_request(request, slug):
    job_request = get_object_or_404(JobRequests, job__slug=slug)
    job_request.status = "Rejeitado"  # Defina o status como 'Rejeitado'
    job_request.save()

    # Atualize também o status de rejeição na tabela de
    # solicitações de candidatos a emprego
    candidate_request = job_request.candidate.requests.filter(job__slug=slug).first()
    if candidate_request:
        candidate_request.status = "Rejeitado"
        candidate_request.save()

    return redirect("company-home")


def hired_status(request, slug):
    req = JobRequests.objects.filter(slug=slug).first()
    req.hired = True
    return redirect("company-home")


def delete_request(request, slug):
    # Obtém a solicitação de emprego pelo slug
    req = get_object_or_404(JobRequests, job__slug=slug)
    req.delete()

    messages.success(request, "Solicitação excluída com sucesso.")
    return redirect("company-home")


def reject_and_delete_request(request, slug):
    job_request = get_object_or_404(JobRequests, job__slug=slug)

    # Rejeitar a solicitação
    job_request.accepted = False
    job_request.save()

    # Excluir a solicitação
    job_request.delete()

    # Atualizar também o status de rejeição na tabela de
    # solicitações de candidatos a emprego
    candidate_request = job_request.candidate.requests.filter(job__slug=slug).first()
    if candidate_request:
        candidate_request.status = "Rejeitado"
        candidate_request.save()

    messages.success(request, "Solicitação rejeitada e excluída com sucesso.")
    return redirect("company-home")
