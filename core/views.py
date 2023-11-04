from datetime import datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import Http404
from django.db.models import Q

from company.models import Job
from .models import User
from .forms import UserRegisterForm, UserLoginForm


def home_page(request):
    jobs = Job.objects.order_by("-created_date").all()
    # convert time
    now = datetime.now(timezone.utc)
    for i in jobs:
        get_days = now - i.created_date
        if get_days.days > 1:
            i.created_date = f"{get_days.days} dias atrás"
    return render(request, "home_page.html", {"jobs": jobs})


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    return render(request, "job_detail.html", {"job": job})


def register(request):
    if request.user.is_authenticated:
        raise Http404

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Verificar se a opção selecionada é "default"
            if data["register_as"] == "default":
                messages.error(
                    request,
                    'Selecione uma opção válida no campo "Cadastrar como"',
                )
            else:
                user = User.objects.create_user(
                    data["email"],
                    data["full_name"],
                    data["password1"],
                )

                # Determine a rota de redirecionamento com base na
                # seleção do campo "register_as"
                if data["register_as"] == "candidate":
                    user.is_candidate = True
                    user.is_company = False
                elif data["register_as"] == "company":
                    user.is_candidate = False
                    user.is_company = True
                user.save()

                messages.success(
                    request,
                    "Cadastro realizado com sucesso, faça login!",
                )
                return redirect("login")  # Redirecionar para a rota de login
    else:
        form = UserRegisterForm()

    # Se chegamos aqui, ocorreu uma validação mal-sucedida,
    # mas reutilizamos o formulário com os dados submetidos
    return render(request, "register.html", {"form": form})


def login_request(request):
    if request.user.is_authenticated:
        raise Http404
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                email=data["email"],
                password=data["password"],
            )
            if user is not None:
                login(request, user)
                # if user is candidate
                if user.is_candidate:
                    return redirect("home-page")
                # if user is a company
                elif not user.is_candidate:
                    return redirect("company-home")
            else:
                messages.error(
                    request,
                    "Nome de usuário ou senha incorretos",
                )
                return redirect("login")
    form = UserLoginForm()
    return render(request, "login.html", {"form": form})


def search(request):
    query = request.GET.get("q")
    results = Job.objects.filter(
        Q(title_icontains=query) | Q(skills_required_icontains=query)
    ).all()

    if not results:
        messages.info(request, "Nenhum resultado encontrado")
    else:
        messages.info(request, f"{results.count()} resultados encontrados")

    now = datetime.now(timezone.utc)
    for i in results:
        get_days = now - i.created_date
        if get_days.days > 1:
            i.created_date = f"{get_days.days} dias atrás"
    return render(request, "home_page.html", {"jobs": results})
