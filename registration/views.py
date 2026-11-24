from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
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
    
def student_dashboard(request):
    search_query = request.GET.get('search', '')
    program_filter = request.GET.get('program', '')

    # 1. Summary Queryset
    summary_students = Student.objects.all()

    if search_query:
        # FIXED: Changed 'name' to 'student_name'
        summary_students = summary_students.filter(student_name__icontains=search_query) | summary_students.filter(email__icontains=search_query)
    if program_filter:
        summary_students = summary_students.filter(program=program_filter)

    total_students = summary_students.count() 
    program_summary = summary_students.values('program').annotate(total=Count('id')).order_by('program') 
    year_summary = summary_students.values('year_level').annotate(total=Count('id')).order_by('year_level') 

    # 2. Table Queryset
    table_students = Student.objects.all()
    
    if search_query:
        # FIXED: Changed 'name' to 'student_name'
        table_students = table_students.filter(student_name__icontains=search_query) | table_students.filter(email__icontains=search_query)
    if program_filter:
        table_students = table_students.filter(program=program_filter)

    return render(
        request,
        'registration/student_dashboard.html',
        {
            'total_students': total_students,
            'program_summary': program_summary,
            'year_summary': year_summary,
            'students': table_students, 
            'search_query': search_query,
            'program_filter': program_filter,
        }
    )