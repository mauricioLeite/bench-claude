from django.shortcuts import render
from developers.models import Developer
from skills.models import Skill, DeveloperSkill


def home(request):
    total_devs = Developer.objects.count()
    total_skills = Skill.objects.count()
    available_count = Developer.objects.filter(availability=True).count()
    learning_count = DeveloperSkill.objects.filter(is_learning=True).values('developer').distinct().count()

    context = {
        'total_devs': total_devs,
        'total_skills': total_skills,
        'available_count': available_count,
        'learning_count': learning_count,
    }
    return render(request, 'home.html', context)
