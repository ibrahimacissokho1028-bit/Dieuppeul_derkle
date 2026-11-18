from django.test import TestCase
from django.urls import reverse

from .models import Teacher


class TeacherPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Teacher.objects.create(
            first_name="Mamadou",
            last_name="Ba",
            email="mamadou.test@ecole.sn",
            subject="Mathématiques",
        )

    def test_teacher_list_uses_database(self):
        response = self.client.get(reverse("teachers:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mamadou Ba")
        self.assertContains(response, "Mathématiques")

    def test_teacher_create_view(self):
        response = self.client.post(reverse("teachers:create"), {
            "first_name": "Awa",
            "last_name": "Sarr",
            "email": "awa.enseignante@ecole.sn",
            "subject": "Anglais",
        })

        self.assertRedirects(response, reverse("teachers:list"))
        self.assertTrue(
            Teacher.objects.filter(email="awa.enseignante@ecole.sn").exists()
        )
