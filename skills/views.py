from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import Skill, DeveloperSkill, SKILL_CATEGORIES
from .forms import SkillForm, DeveloperSkillForm, SkillSearchForm
from developers.models import Developer


def skill_list(request):
    skills = Skill.objects.annotate(developer_count=Count('developer_skills')).order_by('name')
    context = {'skills': skills}
    return render(request, 'skills/list.html', context)


def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f'Skill "{skill.name}" criada com sucesso!')
            return redirect('skill_list')
    else:
        form = SkillForm()
    return render(request, 'skills/create.html', {'form': form})


def developer_skill_add(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        form = DeveloperSkillForm(request.POST)
        if form.is_valid():
            dev_skill = form.save(commit=False)
            dev_skill.developer = developer
            try:
                dev_skill.save()
                messages.success(request, f'Skill "{dev_skill.skill.name}" adicionada com sucesso!')
                return redirect('developer_detail', pk=developer.pk)
            except Exception:
                messages.error(request, 'Você já possui essa skill. Edite a existente.')
    else:
        form = DeveloperSkillForm()
    return render(request, 'skills/add_skill.html', {'form': form, 'developer': developer})


def developer_skill_edit(request, dev_pk, pk):
    developer = get_object_or_404(Developer, pk=dev_pk)
    dev_skill = get_object_or_404(DeveloperSkill, pk=pk, developer=developer)
    if request.method == 'POST':
        form = DeveloperSkillForm(request.POST, instance=dev_skill)
        if form.is_valid():
            form.save()
            messages.success(request, f'Skill "{dev_skill.skill.name}" atualizada com sucesso!')
            return redirect('developer_detail', pk=developer.pk)
    else:
        form = DeveloperSkillForm(instance=dev_skill)
    return render(request, 'skills/edit_skill.html', {'form': form, 'developer': developer, 'dev_skill': dev_skill})


def developer_skill_delete(request, dev_pk, pk):
    developer = get_object_or_404(Developer, pk=dev_pk)
    dev_skill = get_object_or_404(DeveloperSkill, pk=pk, developer=developer)
    if request.method == 'POST':
        skill_name = dev_skill.skill.name
        dev_skill.delete()
        messages.success(request, f'Skill "{skill_name}" removida com sucesso!')
        return redirect('developer_detail', pk=developer.pk)
    return render(request, 'skills/confirm_delete_skill.html', {'developer': developer, 'dev_skill': dev_skill})


def skill_search(request):
    form = SkillSearchForm(request.GET or None)
    developers = None

    if request.GET:
        developers = Developer.objects.prefetch_related('developer_skills__skill').all()
        skill_filter = request.GET.get('skill')
        category_filter = request.GET.get('category')
        type_filter = request.GET.get('type')
        min_level = request.GET.get('min_level')
        team_filter = request.GET.get('team')
        availability = request.GET.get('availability')
        is_learning = request.GET.get('is_learning')

        dev_skill_qs = DeveloperSkill.objects.all()

        if skill_filter:
            dev_skill_qs = dev_skill_qs.filter(skill_id=skill_filter)
        if category_filter:
            dev_skill_qs = dev_skill_qs.filter(skill__category=category_filter)
        if type_filter:
            dev_skill_qs = dev_skill_qs.filter(skill__type=type_filter)
        if min_level:
            dev_skill_qs = dev_skill_qs.filter(level__gte=int(min_level))
        if is_learning:
            dev_skill_qs = dev_skill_qs.filter(is_learning=True)

        matching_dev_ids = dev_skill_qs.values_list('developer_id', flat=True).distinct()
        developers = Developer.objects.filter(pk__in=matching_dev_ids)

        if team_filter:
            developers = developers.filter(team__icontains=team_filter)
        if availability:
            developers = developers.filter(availability=True)

        developers = developers.prefetch_related('developer_skills__skill')

    context = {
        'form': form,
        'developers': developers,
        'searched': bool(request.GET),
    }
    return render(request, 'skills/search.html', context)


def clusters_view(request):
    clusters = [
        {
            'name': 'Front-end',
            'icon': 'bi-browser-chrome',
            'color': 'primary',
            'categories': ['linguagem', 'framework'],
            'type_filter': 'hard',
            'extra_names': ['React', 'Vue', 'Angular', 'HTML', 'CSS', 'JavaScript', 'TypeScript'],
        },
        {
            'name': 'Back-end',
            'icon': 'bi-server',
            'color': 'success',
            'categories': ['linguagem', 'framework'],
            'type_filter': 'hard',
        },
        {
            'name': 'Dados',
            'icon': 'bi-database',
            'color': 'info',
            'categories': ['banco_de_dados'],
            'type_filter': 'hard',
        },
        {
            'name': 'Automação',
            'icon': 'bi-robot',
            'color': 'warning',
            'categories': ['automacao'],
            'type_filter': 'hard',
        },
        {
            'name': 'Low-code',
            'icon': 'bi-puzzle',
            'color': 'secondary',
            'categories': ['low_code'],
            'type_filter': 'hard',
        },
        {
            'name': 'Cloud',
            'icon': 'bi-cloud',
            'color': 'primary',
            'categories': ['cloud'],
            'type_filter': 'hard',
        },
        {
            'name': 'DevOps',
            'icon': 'bi-gear-wide-connected',
            'color': 'danger',
            'categories': ['devops'],
            'type_filter': 'hard',
        },
        {
            'name': 'Soft Skills',
            'icon': 'bi-people',
            'color': 'success',
            'categories': ['comunicacao', 'lideranca', 'didatica', 'organizacao',
                           'resolucao_problemas', 'trabalho_equipe', 'mentoria', 'documentacao', 'metodologia'],
            'type_filter': 'soft',
        },
    ]

    cluster_data = []
    for cluster in clusters:
        skills_qs = Skill.objects.filter(
            category__in=cluster['categories']
        ).annotate(
            dev_count=Count('developer_skills')
        ).order_by('-dev_count', 'name')

        cluster_data.append({
            'name': cluster['name'],
            'icon': cluster['icon'],
            'color': cluster['color'],
            'skills': skills_qs,
            'total_skills': skills_qs.count(),
            'total_devs': Developer.objects.filter(
                developer_skills__skill__category__in=cluster['categories']
            ).distinct().count(),
        })

    context = {'clusters': cluster_data}
    return render(request, 'skills/clusters.html', context)
