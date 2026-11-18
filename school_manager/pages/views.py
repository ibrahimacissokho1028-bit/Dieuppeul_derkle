from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from students.models import Student
from teachers.models import Teacher


def home(request):
    class_distribution = list(
        Student.objects.values("classe")
        .annotate(total=Count("pk"))
        .order_by("classe")
    )
    largest_class = max(
        (item["total"] for item in class_distribution),
        default=0,
    )
    for item in class_distribution:
        item["percentage"] = round(item["total"] / largest_class * 100)

    today = timezone.localdate()
    month_start = today.replace(day=1)
    context = {
        "school_name": "Lycée d'Excellence de Dakar",
        "nb_students": Student.objects.count(),
        "nb_active": Student.objects.filter(active=True).count(),
        "nb_teachers": Teacher.objects.count(),
        "nb_classes": len(class_distribution),
        "new_enrollments": Student.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=today,
        ).count(),
        "class_distribution": class_distribution,
        "recent_students": Student.objects.order_by("-created_at")[:5],
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")
