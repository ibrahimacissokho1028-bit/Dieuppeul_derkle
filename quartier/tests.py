from django.test import TestCase

from .models import EtapeHistoire, MessageContact


class HomeViewTests(TestCase):
    def test_homepage_renders_contact_form_and_sections(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_history_timeline_is_managed_from_admin_content(self):
        EtapeHistoire.objects.create(
            repere="Mémoire",
            titre="Les racines du quartier",
            description="Un récit transmis par ses habitants.",
        )

        response = self.client.get("/")

        self.assertContains(response, "Les racines du quartier")

    def test_contact_form_saves_message_and_redirects(self):
        response = self.client.post(
            "/",
            {
                "nom": "Awa Ndiaye",
                "email": "awa@example.com",
                "message": "Un souvenir du quartier.",
            },
        )

        self.assertRedirects(response, "/?contact=envoye#contact", fetch_redirect_response=False)
        self.assertEqual(MessageContact.objects.count(), 1)
        self.assertEqual(MessageContact.objects.get().nom, "Awa Ndiaye")

    def test_invalid_contact_form_is_rendered_again(self):
        response = self.client.post(
            "/",
            {
                "nom": "",
                "email": "adresse-invalide",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(MessageContact.objects.count(), 0)
        self.assertContains(response, "Ce champ est obligatoire.", status_code=400)
