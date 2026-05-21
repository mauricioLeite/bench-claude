from django.test import TestCase
from django.urls import reverse
from developers.models import Developer
from skills.models import Skill
from .models import ConnectionRequest


class ConnectionTests(TestCase):

    def setUp(self):
        self.developer = Developer.objects.create(
            name='Carlos Mendes',
            email='carlos.mendes@example.com',
            team='DevOps',
            job_title='DevOps Engineer',
            availability=True,
        )
        self.skill = Skill.objects.create(
            name='Kubernetes',
            category='devops',
            type='hard',
        )

    def test_create_connection_request(self):
        url = reverse('connection_create')
        response = self.client.post(url, {
            'requester_name': 'Alice',
            'requester_email': 'alice@example.com',
            'receiver': self.developer.pk,
            'skill': self.skill.pk,
            'message': 'Preciso de ajuda com Kubernetes.',
            'urgency': 'medium',
        })
        self.assertTrue(ConnectionRequest.objects.filter(
            requester_email='alice@example.com'
        ).exists())
        connection = ConnectionRequest.objects.get(requester_email='alice@example.com')
        self.assertEqual(connection.status, 'pending')

    def test_update_status(self):
        connection = ConnectionRequest.objects.create(
            requester_name='Bob',
            requester_email='bob@example.com',
            receiver=self.developer,
            message='Preciso de ajuda.',
            urgency='low',
            status='pending',
        )
        url = reverse('connection_status_update', kwargs={'pk': connection.pk})
        response = self.client.post(url, {'status': 'accepted'})
        connection.refresh_from_db()
        self.assertEqual(connection.status, 'accepted')

        response = self.client.post(url, {'status': 'done'})
        connection.refresh_from_db()
        self.assertEqual(connection.status, 'done')

        response = self.client.post(url, {'status': 'rejected'})
        connection.refresh_from_db()
        self.assertEqual(connection.status, 'rejected')

    def test_connection_list(self):
        ConnectionRequest.objects.create(
            requester_name='Carol',
            requester_email='carol@example.com',
            receiver=self.developer,
            message='Olá!',
            urgency='high',
        )
        url = reverse('connection_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carol')
