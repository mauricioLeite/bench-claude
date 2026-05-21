from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Developer
from .forms import DeveloperForm
from skills.models import DeveloperSkill
from connections.models import Endorsement
from connections.forms import EndorsementForm


def developer_list(request):
    query = request.GET.get('q', '')
    developers = Developer.objects.prefetch_related('developer_skills__skill').all()
    if query:
        developers = developers.filter(
            Q(name__icontains=query) |
            Q(team__icontains=query) |
            Q(job_title__icontains=query)
        )
    context = {
        'developers': developers,
        'query': query,
    }
    return render(request, 'developers/list.html', context)


def developer_create(request):
    if request.method == 'POST':
        form = DeveloperForm(request.POST)
        if form.is_valid():
            developer = form.save()
            messages.success(request, f'Desenvolvedor "{developer.name}" criado com sucesso!')
            return redirect('developer_detail', pk=developer.pk)
    else:
        form = DeveloperForm()
    return render(request, 'developers/create.html', {'form': form})


def developer_edit(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        form = DeveloperForm(request.POST, instance=developer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Perfil de "{developer.name}" atualizado com sucesso!')
            return redirect('developer_detail', pk=developer.pk)
    else:
        form = DeveloperForm(instance=developer)
    return render(request, 'developers/edit.html', {'form': form, 'developer': developer})


def developer_delete(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        name = developer.name
        developer.delete()
        messages.success(request, f'Desenvolvedor "{name}" removido com sucesso!')
        return redirect('developer_list')
    return render(request, 'developers/confirm_delete.html', {'developer': developer})


def developer_detail(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    hard_skills = DeveloperSkill.objects.filter(
        developer=developer,
        skill__type='hard'
    ).select_related('skill').order_by('-level')
    soft_skills = DeveloperSkill.objects.filter(
        developer=developer,
        skill__type='soft'
    ).select_related('skill').order_by('-level')
    endorsements = Endorsement.objects.filter(to_developer=developer).select_related('skill').order_by('-created_at')

    if request.method == 'POST':
        endorsement_form = EndorsementForm(request.POST, developer=developer)
        if endorsement_form.is_valid():
            endorsement = endorsement_form.save(commit=False)
            endorsement.to_developer = developer
            endorsement.save()
            messages.success(request, 'Endorsement enviado com sucesso!')
            return redirect('developer_detail', pk=developer.pk)
    else:
        endorsement_form = EndorsementForm(developer=developer)

    context = {
        'developer': developer,
        'hard_skills': hard_skills,
        'soft_skills': soft_skills,
        'endorsements': endorsements,
        'endorsement_form': endorsement_form,
    }
    return render(request, 'developers/detail.html', context)
