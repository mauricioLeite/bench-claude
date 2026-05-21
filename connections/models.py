from django.db import models

URGENCY_CHOICES = (
    ('low', 'Baixa'),
    ('medium', 'Média'),
    ('high', 'Alta'),
)

STATUS_CHOICES = (
    ('pending', 'Pendente'),
    ('accepted', 'Aceita'),
    ('rejected', 'Recusada'),
    ('done', 'Concluída'),
)


class ConnectionRequest(models.Model):
    requester_name = models.CharField(max_length=200)
    requester_email = models.EmailField()
    receiver = models.ForeignKey(
        'developers.Developer',
        on_delete=models.CASCADE,
        related_name='connection_requests'
    )
    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='connection_requests'
    )
    message = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Solicitação de {self.requester_name} para {self.receiver.name}'


class Endorsement(models.Model):
    from_name = models.CharField(max_length=200)
    to_developer = models.ForeignKey(
        'developers.Developer',
        on_delete=models.CASCADE,
        related_name='endorsements'
    )
    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.CASCADE,
        related_name='endorsements'
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Endorsement de {self.from_name} para {self.to_developer.name} em {self.skill.name}'
