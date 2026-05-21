from django.test import TestCase
from django.urls import reverse
from developers.models import Developer
from .models import Skill, DeveloperSkill


class SkillTests(TestCase):

    def setUp(self):
        self.developer = Developer.objects.create(
            name='Maria Souza',
            email='maria.souza@example.com',
            team='Data',
            job_title='Data Scientist',
            availability=True,
        )
        self.developer2 = Developer.objects.create(
            name='Pedro Lima',
            email='pedro.lima@example.com',
            team='Backend',
            job_title='Backend Developer',
            availability=False,
        )
        self.skill = Skill.objects.create(
            name='Python',
            category='linguagem',
            type='hard',
        )
        self.skill2 = Skill.objects.create(
            name='Comunicação',
            category='comunicacao',
            type='soft',
        )

    def test_create_skill(self):
        url = reverse('skill_create')
        response = self.client.post(url, {
            'name': 'Django',
            'category': 'framework',
            'type': 'hard',
        })
        self.assertTrue(Skill.objects.filter(name='Django').exists())

    def test_add_skill_to_developer(self):
        url = reverse('developer_skill_add', kwargs={'pk': self.developer.pk})
        response = self.client.post(url, {
            'skill': self.skill.pk,
            'level': 3,
            'is_learning': False,
            'is_available_to_help': True,
            'description': 'Uso Python diariamente.',
            'years_of_experience': 3.0,
        })
        self.assertTrue(DeveloperSkill.objects.filter(
            developer=self.developer,
            skill=self.skill
        ).exists())

    def test_no_duplicate_skills(self):
        DeveloperSkill.objects.create(
            developer=self.developer,
            skill=self.skill,
            level=2,
        )
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            DeveloperSkill.objects.create(
                developer=self.developer,
                skill=self.skill,
                level=3,
            )

    def test_search_by_skill(self):
        DeveloperSkill.objects.create(
            developer=self.developer,
            skill=self.skill,
            level=3,
        )
        url = reverse('skill_search')
        response = self.client.get(url, {'skill': self.skill.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Souza')
        self.assertNotContains(response, 'Pedro Lima')

    def test_search_by_min_level(self):
        DeveloperSkill.objects.create(
            developer=self.developer,
            skill=self.skill,
            level=4,
        )
        DeveloperSkill.objects.create(
            developer=self.developer2,
            skill=self.skill,
            level=2,
        )
        url = reverse('skill_search')
        response = self.client.get(url, {'min_level': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Souza')
        self.assertNotContains(response, 'Pedro Lima')

    def test_search_by_availability(self):
        DeveloperSkill.objects.create(
            developer=self.developer,
            skill=self.skill,
            level=2,
        )
        DeveloperSkill.objects.create(
            developer=self.developer2,
            skill=self.skill,
            level=2,
        )
        url = reverse('skill_search')
        response = self.client.get(url, {'availability': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Souza')
        self.assertNotContains(response, 'Pedro Lima')
