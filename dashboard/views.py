from django.shortcuts import render
from django.db.models import Count, Q
from developers.models import Developer
from skills.models import Skill, DeveloperSkill, LEVEL_CHOICES


def dashboard_index(request):
    total_devs = Developer.objects.count()
    total_skills = Skill.objects.count()
    available_count = Developer.objects.filter(availability=True).count()
    learning_count = DeveloperSkill.objects.filter(is_learning=True).values('developer').distinct().count()

    top_skills = Skill.objects.annotate(
        dev_count=Count('developer_skills')
    ).filter(dev_count__gt=0).order_by('-dev_count')[:10]

    max_dev_count = top_skills[0].dev_count if top_skills else 1

    top_skills_with_pct = []
    for skill in top_skills:
        pct = int((skill.dev_count / max_dev_count) * 100) if max_dev_count > 0 else 0
        top_skills_with_pct.append({'skill': skill, 'pct': pct})

    level_distribution = []
    for level_val, level_label in LEVEL_CHOICES:
        count = DeveloperSkill.objects.filter(level=level_val).count()
        level_distribution.append({'level': level_val, 'label': level_label, 'count': count})

    few_experts = Skill.objects.annotate(
        expert_count=Count(
            'developer_skills',
            filter=Q(developer_skills__level__gte=4)
        )
    ).filter(expert_count__lt=2, developer_skills__isnull=False).distinct().order_by('expert_count', 'name')[:10]

    context = {
        'total_devs': total_devs,
        'total_skills': total_skills,
        'available_count': available_count,
        'learning_count': learning_count,
        'top_skills': top_skills_with_pct,
        'level_distribution': level_distribution,
        'few_experts': few_experts,
    }
    return render(request, 'dashboard/index.html', context)
