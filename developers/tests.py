from django.test import TestCase
from django.urls import reverse
from .models import Developer


class DeveloperTests(TestCase):

    def setUp(self):
        self.developer_data = {
            'name': 'Ana Silva',
            'email': 'ana.silva@example.com',
            'team': 'Backend',
            'job_title': 'Engenheira de Software',
            'bio': 'Desenvolvedora Python com 5 anos de experiência.',
            'availability': True,
            'avatar_url': '',
        }
        self.developer = Developer.objects.create(
            name='João Santos',
            email='joao.santos@example.com',
            team='Frontend',
            job_title='Desenvolvedor Frontend',
            availability=True,
        )

    def test_create_developer(self):
        url = reverse('developer_create')
        response = self.client.post(url, self.developer_data)
        self.assertEqual(Developer.objects.filter(email='ana.silva@example.com').count(), 1)
        developer = Developer.objects.get(email='ana.silva@example.com')
        self.assertRedirects(response, reverse('developer_detail', kwargs={'pk': developer.pk}))

    def test_list_developers(self):
        url = reverse('developer_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Santos')

    def test_developer_detail(self):
        url = reverse('developer_detail', kwargs={'pk': self.developer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Santos')

    def test_edit_developer(self):
        url = reverse('developer_edit', kwargs={'pk': self.developer.pk})
        updated_data = {
            'name': 'João Santos Atualizado',
            'email': 'joao.santos@example.com',
            'team': 'Backend',
            'job_title': 'Engenheiro Sênior',
            'bio': '',
            'availability': True,
            'avatar_url': '',
        }
        response = self.client.post(url, updated_data)
        self.developer.refresh_from_db()
        self.assertEqual(self.developer.name, 'João Santos Atualizado')
        self.assertEqual(self.developer.team, 'Backend')

    def test_delete_developer(self):
        url = reverse('developer_delete', kwargs={'pk': self.developer.pk})
        response = self.client.post(url)
        self.assertFalse(Developer.objects.filter(pk=self.developer.pk).exists())
        self.assertRedirects(response, reverse('developer_list'))
