from django.test import TestCase
from django.urls import reverse


class GeneralPagesTests(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["school_name"],
            "Lycée d'Excellence de Dakar",
        )

    def test_about_page(self):
        response = self.client.get(reverse("pages:about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "À propos de School Manager")
