from django import forms
from .models import Developer


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'email', 'team', 'job_title', 'bio', 'availability', 'avatar_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@empresa.com'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Backend, Data, DevOps'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Engenheiro de Software Sênior'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você...'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
        labels = {
            'name': 'Nome',
            'email': 'E-mail',
            'team': 'Time/Equipe',
            'job_title': 'Cargo',
            'bio': 'Bio',
            'availability': 'Disponível para ajudar',
            'avatar_url': 'URL do Avatar',
        }
