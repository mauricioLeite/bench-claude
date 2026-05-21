from django.test import TestCase
from django.urls import reverse
from developers.models import Developer
from skills.models import Skill, DeveloperSkill


class DashboardTests(TestCase):

    def setUp(self):
        self.developer1 = Developer.objects.create(
            name='Lucas Ferreira',
            email='lucas.ferreira@example.com',
            team='Backend',
            job_title='Developer',
            availability=True,
        )
        self.developer2 = Developer.objects.create(
            name='Sofia Carvalho',
            email='sofia.carvalho@example.com',
            team='Frontend',
            job_title='Designer',
            availability=False,
        )
        self.skill = Skill.objects.create(
            name='JavaScript',
            category='linguagem',
            type='hard',
        )
        DeveloperSkill.objects.create(
            developer=self.developer1,
            skill=self.skill,
            level=3,
        )

    def test_dashboard_loads(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_shows_stats(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_devs', response.context)
        self.assertIn('total_skills', response.context)
        self.assertEqual(response.context['total_devs'], 2)
        self.assertEqual(response.context['total_skills'], 1)
        self.assertContains(response, '2')
        self.assertContains(response, '1')
