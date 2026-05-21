from django import forms
from .models import ConnectionRequest, Endorsement
from developers.models import Developer
from skills.models import Skill


class ConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = ['requester_name', 'requester_email', 'receiver', 'skill', 'message', 'urgency']
        widgets = {
            'requester_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'requester_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'receiver': forms.Select(attrs={'class': 'form-select'}),
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o que você precisa de ajuda...'
            }),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'requester_name': 'Seu nome',
            'requester_email': 'Seu e-mail',
            'receiver': 'Desenvolvedor',
            'skill': 'Skill relacionada',
            'message': 'Mensagem',
            'urgency': 'Urgência',
        }


class EndorsementForm(forms.ModelForm):
    class Meta:
        model = Endorsement
        fields = ['from_name', 'skill', 'comment']
        widgets = {
            'from_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deixe um comentário sobre essa skill...'
            }),
        }
        labels = {
            'from_name': 'Seu nome',
            'skill': 'Skill',
            'comment': 'Comentário',
        }

    def __init__(self, *args, **kwargs):
        developer = kwargs.pop('developer', None)
        super().__init__(*args, **kwargs)
        if developer:
            skill_ids = developer.developer_skills.values_list('skill_id', flat=True)
            self.fields['skill'].queryset = Skill.objects.filter(pk__in=skill_ids)
