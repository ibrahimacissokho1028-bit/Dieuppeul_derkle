from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def student_list(request):
    query = request.GET.get("q", "")
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    return render(
        request,
        "students/student_list.html",
        {"students": students, "query": query},
    )


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "students/student_detail.html", {"student": student})


def students_by_class(request, classe):
    students = Student.objects.filter(classe=classe)
    return render(
        request,
        "students/student_list.html",
        {"students": students, "classe": classe, "query": ""},
    )


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"{student} a été inscrit(e).")
            return redirect("students:detail", id=student.id)
    else:
        form = StudentForm()
    context = {"form": form, "title": "Inscrire un étudiant"}
    return render(request, "students/student_form.html", context)


def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"La fiche de {student} a été mise à jour.")
            return redirect("students:detail", id=student.id)
    else:
        form = StudentForm(instance=student)
    context = {"form": form, "title": f"Modifier {student}", "student": student}
    return render(request, "students/student_form.html", context)


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        name = str(student)
        student.delete()
        messages.success(request, f"{name} a été supprimé(e).")
        return redirect("students:list")
    context = {"student": student}
    return render(request, "students/student_confirm_delete.html", context)
