from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "muhriddin",
                "first_name": "Muhriddin",
                "last_name": "Bozorov",
                "email": "muhriddin@mail.com",
                "password": "birnima"
            }
        )

        user = CustomUser.objects.get(username="muhriddin")

        self.assertEqual(user.first_name, "Muhriddin")
        self.assertEqual(user.last_name, "Bozorov")
        self.assertEqual(user.email, "muhriddin@mail.com")
        self.assertNotEqual(user.password, "birnima")
        self.assertTrue(user.check_password("birnima"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Muhriddin",
                "email": "muhriddin@mail.com"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "muhriddin",
                "first_name": "Muhriddin",
                "last_name": "Bozorov",
                "email": "invalid email",
                "password": "birnima"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username = "muhriddin", first_name = "Muhriddin" )
        user.set_password("birnima")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "muhriddin",
                "first_name": "Muhriddin",
                "last_name": "Bozorov",
                "email": "invalid email",
                "password": "birnima"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(response, "form", "username", 'A user with that username already exists.')
