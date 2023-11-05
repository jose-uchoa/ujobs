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


@login_required
@user_passes_test(is_company)
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


@login_required
@user_passes_test(is_company)
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


@login_required
@user_passes_test(is_company)
def company_jobs(request):
    # Mostrar todos os empregos publicados pelo empregador/empresa.
    try:
        jobs = request.user.company.jobs.all()

        now = datetime.now(timezone.utc)
        for i in jobs:
            get_days = now - i.created_date
            if get_days.days > 1:
                i.created_date = f"{get_days.days} dias atrás"

        # Criar um dicionário para armazenar o número de pedidos de cada trabalho
        job_requests_dict = {}
        for job in jobs:
            job_requests_count = JobRequests.objects.filter(
                company=request.user.company, job=job
            ).count()
            job_requests_dict[job.id] = job_requests_count

    except Company.DoesNotExist:
        return redirect("company-home")

    return render(
        request, "jobs.html", {"jobs": jobs, "job_requests_dict": job_requests_dict}
    )


@login_required
@user_passes_test(is_company)
def job_candidates_view(request, slug):
    # Obtém o job pelo slug
    job = get_object_or_404(Job, slug=slug, company=request.user.company)

    # Obtém todas as solicitações de emprego para essa vaga
    job_requests = JobRequests.objects.filter(job=job)

    return render(
        request, "job_candidates.html", {"job": job, "job_requests": job_requests}
    )


@login_required
@user_passes_test(is_company)
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


def accepted_status(request, request_id, slug):
    job_request = get_object_or_404(JobRequests, id=request_id, job__slug=slug)
    job_request.accepted = True
    job_request.status = "Aprovado"  # Defina o status como 'Aprovado'
    job_request.save()

    # Atualize também o status de aceitação na tabela de
    # solicitações de candidatos a emprego
    candidate_request = job_request.candidate.requests.filter(
        job__slug=slug,
    ).first()

    if candidate_request:
        candidate_request.status = "Aprovado"
        candidate_request.save()

    messages.success(request, "Solicitação aceita com sucesso.")

    # Verifique o referente para determinar a origem
    referer = request.META.get('HTTP_REFERER', None)

    # Verifique se a URL referente corresponde à rota de candidatos para um job específico
    if referer and f"/company/job/{slug}/candidates/" in referer:
        return redirect('job-candidates', slug=slug)
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


def reject_and_delete_request(request, request_id, slug):
    job_request = get_object_or_404(JobRequests, id=request_id, job__slug=slug)

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

    # Verifique o referente para determinar a origem
    referer = request.META.get('HTTP_REFERER', None)

    # Verifique se a URL referente corresponde à rota de candidatos para um job específico
    if referer and f"/company/job/{slug}/candidates/" in referer:
        return redirect('job-candidates', slug=slug)
    return redirect("company-home")
