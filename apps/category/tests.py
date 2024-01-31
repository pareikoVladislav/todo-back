from django.test import TestCase
from rest_framework import status
from apps.category.models import Category
from apps.user.models import User
from rest_framework.test import APIClient
from apps.category.success_messages import NEW_CATEGORY_CREATED_MESSAGE


class CategoryListGenericViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )

        self.category = Category.objects.create(
            name='Test category'
        )
        self.client = APIClient()

    def test_get_categories(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['category'], str)
        self.assertEqual(Category.objects.count(), 1)
        self.assertContains(response, self.category)

    def test_get_categories_no_content(self):
        self.client.force_authenticate(user=self.user)
        Category.objects.all().delete()
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/categories/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_category_valid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test Category'
        }
        response = self.client.post(f'http://127.0.0.1:8000/api/v1/categories/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], NEW_CATEGORY_CREATED_MESSAGE)
        self.assertEqual(response.data['data']['name'], 'Test Category')
        self.assertTrue(Category.objects.filter(name='Test Category').exists())

    def test_post_category_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': ''
        }
        response = self.client.post(f'http://127.0.0.1:8000/api/v1/categories/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(Category.objects.count(), 0)