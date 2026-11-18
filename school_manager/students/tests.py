from django.test import TestCase
from django.urls import reverse

from .forms import StudentForm
from .models import Student


class StudentPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.awa = Student.objects.create(
            first_name="Awa",
            last_name="Diop",
            email="awa.test@ecole.sn",
            classe="L1",
            active=True,
        )
        Student.objects.create(
            first_name="Fatou",
            last_name="Ndiaye",
            email="fatou.test@ecole.sn",
            classe="L1",
            active=False,
        )
        Student.objects.create(
            first_name="Moussa",
            last_name="Fall",
            email="moussa.test@ecole.sn",
            classe="L2",
            active=True,
        )

    def test_student_list_shows_students_from_database(self):
        response = self.client.get(reverse("students:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Awa")
        self.assertContains(response, "Fatou")
        self.assertContains(response, "Moussa")

    def test_search_matches_first_or_last_name(self):
        response = self.client.get(reverse("students:list"), {"q": "di"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Awa")
        self.assertContains(response, "Fatou")
        self.assertNotContains(response, "Moussa")
        self.assertContains(response, 'value="di"')

    def test_student_detail_and_missing_student(self):
        response = self.client.get(
            reverse("students:detail", args=[self.awa.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "awa.test@ecole.sn")

        missing = self.client.get(reverse("students:detail", args=[999]))
        self.assertEqual(missing.status_code, 404)

    def test_class_filter(self):
        response = self.client.get(
            reverse("students:by_class", args=["L1"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Awa")
        self.assertContains(response, "Fatou")
        self.assertNotContains(response, "Moussa")

    def test_homepage_counts_students_and_active_students(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["nb_students"], 3)
        self.assertEqual(response.context["nb_active"], 2)

    def test_orm_read_create_save_and_delete_operations(self):
        self.assertEqual(Student.objects.all().count(), 3)
        self.assertEqual(
            Student.objects.get(email="awa.test@ecole.sn").first_name,
            "Awa",
        )
        self.assertEqual(Student.objects.filter(classe="L1").count(), 2)

        student = Student.objects.create(
            first_name="Khady",
            last_name="Gueye",
            email="khady.test@ecole.sn",
            classe="L1",
        )
        self.assertEqual(Student.objects.count(), 4)

        student.classe = "L2"
        student.save()
        student.refresh_from_db()
        self.assertEqual(student.classe, "L2")

        student.delete()
        self.assertEqual(Student.objects.count(), 3)

    def test_student_form_rejects_duplicate_email_and_invalid_phone(self):
        duplicate = StudentForm(data={
            "first_name": "Autre",
            "last_name": "Étudiant",
            "email": "awa.test@ecole.sn",
            "classe": "L1",
            "phone": "77 123 45 67",
            "active": True,
        })
        self.assertFalse(duplicate.is_valid())
        self.assertIn("email", duplicate.errors)

        invalid_phone = StudentForm(data={
            "first_name": "Aminata",
            "last_name": "Faye",
            "email": "aminata.test@ecole.sn",
            "classe": "L1",
            "phone": "77-12",
            "active": True,
        })
        self.assertFalse(invalid_phone.is_valid())
        self.assertIn("phone", invalid_phone.errors)

    def test_student_create_update_and_delete_views(self):
        create_response = self.client.post(reverse("students:create"), {
            "first_name": "Aminata",
            "last_name": "Faye",
            "email": "aminata.test@ecole.sn",
            "classe": "L1",
            "phone": "77 123 45 67",
            "active": "on",
        })
        student = Student.objects.get(email="aminata.test@ecole.sn")
        self.assertRedirects(
            create_response,
            reverse("students:detail", args=[student.pk]),
        )
        self.assertEqual(student.phone, "771234567")

        update_response = self.client.post(
            reverse("students:update", args=[student.pk]),
            {
                "first_name": "Aminata",
                "last_name": "Faye",
                "email": "aminata.test@ecole.sn",
                "classe": "L2",
                "phone": "771234567",
                "active": "on",
            },
        )
        self.assertRedirects(
            update_response,
            reverse("students:detail", args=[student.pk]),
        )
        student.refresh_from_db()
        self.assertEqual(student.classe, "L2")

        confirm_response = self.client.get(
            reverse("students:delete", args=[student.pk])
        )
        self.assertEqual(confirm_response.status_code, 200)
        self.assertContains(confirm_response, "Supprimer Aminata Faye")

        delete_response = self.client.post(
            reverse("students:delete", args=[student.pk])
        )
        self.assertRedirects(delete_response, reverse("students:list"))
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())
