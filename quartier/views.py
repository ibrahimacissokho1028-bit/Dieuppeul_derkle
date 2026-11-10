from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .forms import MessageContactForm
from .models import ChiffreCle, EtapeHistoire, Evenement, Lieu, PhotoGalerie, Temoignage


class HomeView(View):
    template_name = "quartier/home.html"

    def get_context_data(self, form=None):
        return {
            "etapes_histoire": EtapeHistoire.objects.all(),
            "lieux": Lieu.objects.all(),
            "evenements": Evenement.objects.filter(date__gte=timezone.now()),
            "photos": PhotoGalerie.objects.all(),
            "temoignages": Temoignage.objects.all(),
            "chiffres": ChiffreCle.objects.all(),
            "form": form or MessageContactForm(),
        }

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                **self.get_context_data(),
                "contact_envoye": request.GET.get("contact") == "envoye",
            },
        )

    def post(self, request):
        form = MessageContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('home')}?contact=envoye#contact")
        return render(
            request,
            self.template_name,
            {**self.get_context_data(form=form), "contact_envoye": False},
            status=400,
        )
