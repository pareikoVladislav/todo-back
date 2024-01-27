import re
from datetime import datetime

from django.test import TestCase
from apps.user.models import User
from rest_framework.test import APIClient
from rest_framework import status


class ListUsersGenericViewTest(TestCase):
    # работают наши разрешения (админ)
    # если всё работает - что данные отображаются (поле соответствует типу данных)
    # если всё работает, но самих пользователей нет
    datetime_regex = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z')

    def setUp(self):
        # прописываем какие-либо настройки.
        # которые должны будут примениться преред
        # запуском тест-кейса
        self.user = User.objects.create_user(
            email='test.email@yahoo.com',
            first_name='Vlad',
            last_name='Test',
            username='vladT',
            password='qWeRtY'
        )
        self.admin = User.objects.create_superuser(
            email='test.admin@gmail.com',
            first_name='ADMIN',
            last_name='TEST',
            username='AdMiNtEsT',
            password='qWeRtYadmin',
            is_staff=True,
            is_superuser=True
        )

        self.client = APIClient()

    def test_get_users_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), User.objects.count() - 1)

        for user in response.data:
            self.assertIsInstance(user['email'], str)
            self.assertIsInstance(user['first_name'], str)
            self.assertIsInstance(user['last_name'], str)
            self.assertIsInstance(user['username'], str)
            self.assertIsInstance(user['phone'], (str | None))
            self.assertIsInstance(user['is_staff'], bool)
            self.assertIsInstance(user['is_superuser'], bool)
            self.assertIsInstance(user['is_verified'], bool)
            self.assertIsInstance(user['is_active'], bool)
            self.assertTrue(
                self.datetime_regex.match(
                    user['date_joined']
                ),
                datetime
            )
            self.assertTrue(
                self.datetime_regex.match(
                    user['last_login']
                ),
                datetime
            )

    def test_get_users_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_no_users(self):
        self.client.force_authenticate(user=self.admin)

        User.objects.all().delete()

        response = self.client.get('http://127.0.0.1:8000/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response.data, list)
