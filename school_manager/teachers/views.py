from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeacherForm
from .models import Teacher


def teacher_list(request):
    query = request.GET.get("q", "").strip()
    teachers = Teacher.objects.all()
    if query:
        teachers = teachers.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(subject__icontains=query)
        )
    page_obj = Paginator(teachers, 10).get_page(request.GET.get("page"))
    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
        },
    )


def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    return render(request, "teachers/teacher_detail.html", {"teacher": teacher})


def teacher_create(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"{teacher} a été ajouté(e).")
            return redirect("teachers:list")
    else:
        form = TeacherForm()
    context = {"form": form, "title": "Ajouter un enseignant"}
    return render(request, "teachers/teacher_form.html", context)


def teacher_update(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f"La fiche de {teacher} a été mise à jour.")
            return redirect("teachers:detail", id=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)
    return render(
        request,
        "teachers/teacher_form.html",
        {"form": form, "title": f"Modifier {teacher}", "teacher": teacher},
    )


def teacher_delete(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    if request.method == "POST":
        name = str(teacher)
        teacher.delete()
        messages.success(request, f"{name} a été supprimé(e).")
        return redirect("teachers:list")
    return render(
        request,
        "teachers/teacher_confirm_delete.html",
        {"teacher": teacher},
    )
