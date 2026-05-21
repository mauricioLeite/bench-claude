from django import forms
from .models import Skill, DeveloperSkill, SKILL_CATEGORIES, SKILL_TYPES, LEVEL_CHOICES


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Python, React, Scrum'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Nome da Skill',
            'category': 'Categoria',
            'type': 'Tipo',
        }


class DeveloperSkillForm(forms.ModelForm):
    class Meta:
        model = DeveloperSkill
        fields = ['skill', 'level', 'is_learning', 'is_available_to_help', 'description', 'years_of_experience']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'is_learning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available_to_help': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva sua experiência com essa skill...'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0',
                'placeholder': 'Ex: 2.5'
            }),
        }
        labels = {
            'skill': 'Skill',
            'level': 'Nível',
            'is_learning': 'Estou aprendendo atualmente',
            'is_available_to_help': 'Disponível para ajudar outros',
            'description': 'Descrição da experiência',
            'years_of_experience': 'Anos de experiência',
        }


class SkillSearchForm(forms.Form):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        empty_label='Todas as skills',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Skill',
    )
    category = forms.ChoiceField(
        choices=[('', 'Todas as categorias')] + list(SKILL_CATEGORIES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria',
    )
    type = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + list(SKILL_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo',
    )
    min_level = forms.ChoiceField(
        choices=[('', 'Qualquer nível')] + list(LEVEL_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Nível mínimo',
    )
    team = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Backend, Data'}),
        label='Time',
    )
    availability = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Disponível para ajudar',
    )
    is_learning = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Aprendendo atualmente',
    )
