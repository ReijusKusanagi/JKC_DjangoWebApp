from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student

# Create operation
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(
        request,
        'registration/student_form.html',
        {'form': form}
    )

# Read operation
def student_list(request):
    students = Student.objects.all()
    return render(
        request,
        'registration/student_list.html',
        {'students': students}
    )

# Update operation
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(
        request,
        'registration/student_form.html',
        {
            'form': form,
            'student': student
        }
    )

# Delete operation
def student_delete(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    return render(
        request,
        'registration/student_confirm_delete.html',
        {'student': student}
    )