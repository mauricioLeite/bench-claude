from django.db import models

SKILL_CATEGORIES = (
    ('linguagem', 'Linguagem'),
    ('framework', 'Framework'),
    ('banco_de_dados', 'Banco de dados'),
    ('cloud', 'Cloud'),
    ('devops', 'DevOps'),
    ('automacao', 'Automação'),
    ('low_code', 'Low-code'),
    ('ferramenta', 'Ferramenta'),
    ('metodologia', 'Metodologia'),
    ('comunicacao', 'Comunicação'),
    ('lideranca', 'Liderança'),
    ('didatica', 'Didática'),
    ('organizacao', 'Organização'),
    ('resolucao_problemas', 'Resolução de problemas'),
    ('trabalho_equipe', 'Trabalho em equipe'),
    ('mentoria', 'Mentoria'),
    ('documentacao', 'Documentação'),
)

SKILL_TYPES = (
    ('hard', 'Hard Skill'),
    ('soft', 'Soft Skill'),
)

LEVEL_CHOICES = (
    (1, 'Estou aprendendo'),
    (2, 'Sei o básico'),
    (3, 'Uso em tarefas reais'),
    (4, 'Tenho experiência avançada'),
    (5, 'Posso ensinar ou mentorar'),
)


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=SKILL_CATEGORIES)
    type = models.CharField(max_length=10, choices=SKILL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DeveloperSkill(models.Model):
    developer = models.ForeignKey(
        'developers.Developer',
        on_delete=models.CASCADE,
        related_name='developer_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='developer_skills'
    )
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    is_learning = models.BooleanField(default=False)
    is_available_to_help = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    years_of_experience = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('developer', 'skill')
        ordering = ['-level', 'skill__name']

    def __str__(self):
        return f'{self.developer.name} - {self.skill.name} (Nível {self.level})'
