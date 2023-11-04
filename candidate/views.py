from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from company.models import Job, JobRequests
from .forms import CandidateProfileForm, CandidateResumeForm
from .models import CandidateProfile, CandidateRequests


def is_candidate(user):
    try:
        if not user.is_candidate:
            raise Http404
        return True
    except Http404:
        raise Http404


@user_passes_test(is_candidate)
@login_required
def candidate_profile(request):
    CandidateProfile.objects.get_or_create(candidate=request.user)
    if request.method == "POST":
        profile_form = CandidateProfileForm(
            request.POST,
            instance=request.user,
        )
        resume_form = CandidateResumeForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid() and resume_form.is_valid():
            profile_form.save()
            resume_form.save()
            messages.success(request, "Seu perfil foi atualizado")
            return redirect("candidate-profile")
    else:
        profile_form = CandidateProfileForm(instance=request.user)
        resume_form = CandidateResumeForm(instance=request.user.profile)
    context = {
        "profile_form": profile_form,
        "resume_form": resume_form,
    }
    return render(request, "candidate_profile.html", context)


@login_required
@user_passes_test(is_candidate)
def request_job(request, slug):
    # Verificar se já existe uma solicitação do usuário para esta vaga
    job = get_object_or_404(Job, slug=slug)
    if request.user.requests.filter(job=job).exists():
        messages.warning(
            request,
            "Você já enviou um currículo para este anúncio anteriormente.",
        )
        return redirect("home-page")

    # Verificar se o usuário tem um currículo carregado
    if not request.user.profile.resume:
        messages.info(request, "Faça o upload do seu currículo primeiro.")
        return redirect("candidate-profile")

    # Criar a solicitação do usuário para a vaga e enviar a solicitação ao empregador
    req = CandidateRequests(job=job, requests=request.user)
    req.save()
    req_to_employer = JobRequests(
        candidate=request.user,
        job=job,
        resume_url=request.user.profile.resume.url,
        employer=job.company,
    )
    req_to_employer.save()
    messages.success(request, "Seu currículo foi enviado")
    return redirect("home-page")


@login_required
@user_passes_test(is_candidate)
def candidate_requests(request):
    requests = request.user.requests.all()
    if not requests:
        messages.info(request, "Você ainda não enviou nenhuma solicitação")
    return render(request, "candidate_requests.html", {"requests": requests})


@login_required
@user_passes_test(is_candidate)
def cancel_request(request, slug):
    candidate_req = get_object_or_404(
        CandidateRequests, job__slug=slug, requests=request.user
    )

    # request sent to employer
    if candidate_req.status != "Aprovado":
        # Não é necessário filtrar novamente, basta excluir o objeto
        candidate_req.delete()
        messages.success(request, "Sua solicitação foi cancelada")
    else:
        raise Http404
    return redirect("candidate-requests")
