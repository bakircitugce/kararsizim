from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import SignupForm


User = get_user_model()


class SignupFormTests(TestCase):
    def test_valid_signup_normalizes_email(self):
        form = SignupForm(
            data={
                "username": "Kararsiz",
                "email": "  USER@Example.COM ",
                "password1": "Strong-password-123!",
                "password2": "Strong-password-123!",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.email, "user@example.com")

    def test_duplicate_email_is_case_insensitive(self):
        User.objects.create_user(
            username="firstuser",
            email="user@example.com",
            password="Strong-password-123!",
        )
        form = SignupForm(
            data={
                "username": "seconduser",
                "email": "USER@EXAMPLE.COM",
                "password1": "Strong-password-123!",
                "password2": "Strong-password-123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Bu e-posta zaten kayıtlı.", form.errors["email"])

    def test_duplicate_username_is_case_insensitive(self):
        User.objects.create_user(
            username="Ali",
            email="ali@example.com",
            password="Strong-password-123!",
        )
        form = SignupForm(
            data={
                "username": "ali",
                "email": "other@example.com",
                "password1": "Strong-password-123!",
                "password2": "Strong-password-123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Bu kullanıcı adı alınmış.", form.errors["username"])

    def test_invalid_username_format_is_rejected(self):
        form = SignupForm(
            data={
                "username": "ab-",
                "email": "user@example.com",
                "password1": "Strong-password-123!",
                "password2": "Strong-password-123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Kullanıcı adı 3-20 karakter olmalı", form.errors["username"][0])


class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="Strong-password-123!",
        )

    def test_signup_logs_user_in_and_does_not_expose_email_in_homepage(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "Strong-password-123!",
                "password2": "Strong-password-123!",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        homepage = self.client.get(reverse("home"))
        self.assertNotContains(homepage, "new@example.com")
        self.assertContains(homepage, "@newuser")

    def test_login_accepts_email_and_redirects_to_safe_next(self):
        response = self.client.post(
            f"{reverse('login')}?next=/",
            {"email": "USER@EXAMPLE.COM", "password": "Strong-password-123!"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login_shows_turkish_error(self):
        response = self.client.post(
            reverse("login"),
            {"email": "user@example.com", "password": "wrong-password"},
        )
        self.assertContains(response, "E-posta veya parola hatalı.")

    def test_external_next_is_not_allowed(self):
        response = self.client.post(
            reverse("login") + "?next=https://example.com",
            {"email": "user@example.com", "password": "Strong-password-123!"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        get_response = self.client.get(reverse("logout"))
        self.assertRedirects(get_response, reverse("home"))
        self.assertTrue(get_response.wsgi_request.user.is_authenticated)

        post_response = self.client.post(reverse("logout"))
        self.assertRedirects(post_response, reverse("home"))
        self.assertFalse(post_response.wsgi_request.user.is_authenticated)

    def test_authenticated_user_is_redirected_from_auth_pages(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("signup")), reverse("home"))
        self.assertRedirects(self.client.get(reverse("login")), reverse("home"))
