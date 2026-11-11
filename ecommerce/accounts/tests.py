from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class RegistrationTests(TestCase):
    def register(self, username='customer', phone='99112233'):
        return self.client.post(reverse('register'), {
            'first_name': 'Test', 'last_name': 'Customer',
            'username': username, 'email': f'{username}@example.com',
            'password': 'test-password-123',
            'confirm_password': 'test-password-123', 'phone_number': phone,
        })

    def test_registration_saves_phone(self):
        self.assertRedirects(self.register(), reverse('signin'))
        profile = UserProfile.objects.get(phone_number='99112233')
        self.assertEqual(profile.user.username, 'customer')
        self.assertTrue(profile.user.check_password('test-password-123'))

    def test_duplicate_phone_is_rejected(self):
        self.register()
        response = self.register(username='another')
        self.assertRedirects(response, reverse('register'))
        self.assertFalse(User.objects.filter(username='another').exists())
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_formatted_mongolian_phone_is_also_duplicate(self):
        self.register()
        response = self.register(username='another', phone='+976 9911-2233')
        self.assertRedirects(response, reverse('register'))
        self.assertEqual(User.objects.count(), 1)

    def test_invalid_phone_is_rejected(self):
        for phone in ('', 'abc99112233', '123', '++99112233'):
            with self.subTest(phone=phone):
                self.assertRedirects(self.register(phone=phone), reverse('register'))
        self.assertEqual(User.objects.count(), 0)

    def test_concurrent_duplicate_does_not_leave_user(self):
        with patch('accounts.views.UserProfile.objects.create', side_effect=IntegrityError):
            self.assertRedirects(self.register(), reverse('register'))
        self.assertEqual(User.objects.count(), 0)

    def test_account_links_are_absolute_on_nested_pages(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'href="/accounts/signin/"')
        self.assertContains(response, 'href="/accounts/register/"')
        self.assertNotContains(response, 'href="accounts/')
        user = User.objects.create_user(username='signed-in', password='test-password')
        self.client.force_login(user)
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'href="/accounts/profile/"')
