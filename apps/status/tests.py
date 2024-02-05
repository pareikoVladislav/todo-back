from django.test import TestCase
from rest_framework import status
from apps.status.models import Status
from apps.user.models import User
from rest_framework.test import APIClient
from apps.status.success_messages import (
    NEW_STATUS_CREATED_MESSAGE,
    STATUS_UPDATED_SUCCESSFULLY_MESSAGE,
    STATUS_WAS_DELETED_SUCCESSFUL,
)


class TestStatusListGenericView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )

        self.status = Status.objects.create(
            name='Test status'
        )
        self.client = APIClient()

    def test_get_statuses(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/statuses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['status'], str)
        self.assertEqual(Status.objects.count(), 1)
        self.assertContains(response, self.status)

    def test_get_statuses_no_content(self):
        self.client.force_authenticate(user=self.user)
        Status.objects.all().delete()
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/statuses/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_status_valid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Status'
        }
        response = self.client.post(f'http://127.0.0.1:8000/api/v1/statuses/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], NEW_STATUS_CREATED_MESSAGE)
        self.assertEqual(response.data['data']['name'], 'New Status')
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_post_status_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': ''
        }
        response = self.client.post(f'http://127.0.0.1:8000/api/v1/statuses/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(Status.objects.count(), 0)
