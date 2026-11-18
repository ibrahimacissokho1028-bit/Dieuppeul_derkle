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

    def test_teacher_search_matches_subject(self):
        response = self.client.get(reverse("teachers:list"), {"q": "Math"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mamadou Ba")
        self.assertContains(response, 'value="Math"')

    def test_teacher_detail_update_and_confirmed_delete(self):
        teacher = Teacher.objects.get(email="mamadou.test@ecole.sn")
        detail = self.client.get(
            reverse("teachers:detail", args=[teacher.pk])
        )
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "Mathématiques")

        update = self.client.post(
            reverse("teachers:update", args=[teacher.pk]),
            {
                "first_name": "Mamadou",
                "last_name": "Ba",
                "email": "mamadou.test@ecole.sn",
                "subject": "Physique",
            },
        )
        self.assertRedirects(
            update,
            reverse("teachers:detail", args=[teacher.pk]),
        )
        teacher.refresh_from_db()
        self.assertEqual(teacher.subject, "Physique")

        confirm = self.client.get(
            reverse("teachers:delete", args=[teacher.pk])
        )
        self.assertEqual(confirm.status_code, 200)
        self.assertTrue(Teacher.objects.filter(pk=teacher.pk).exists())

        delete = self.client.post(
            reverse("teachers:delete", args=[teacher.pk])
        )
        self.assertRedirects(delete, reverse("teachers:list"))
        self.assertFalse(Teacher.objects.filter(pk=teacher.pk).exists())
