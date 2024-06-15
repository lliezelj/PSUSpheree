from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, College, Program, Student
from studentorg.forms import OrganizationForm, OrgMemberForm, CollegeForm, ProgramForm, StudentForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
from django.db.models import Count



@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

# Create your views here.
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name  = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
         qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None:
             query = self.request.GET.get('q')
             qs = qs = qs.filter(Q(name__icontains=query) |
                           Q(description__icontains=query) | Q(college__college_name__icontains=query))
         return qs


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name  = 'orgmember_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_list'] = Organization.objects.all()  
        return context

    def get_queryset(self, *args, **kwargs):
         qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None:
             query = self.request.GET.get('q')
             qs = qs = qs.filter(Q(date_joined__icontains=query) |
                           Q(organization__name__icontains=query) | Q(student__firstname__icontains=query) | Q(student__lastname__icontains=query))
         return qs
    

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')




class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name  = 'college_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = College.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
         qs = super(CollegeList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None:
             query = self.request.GET.get('q')
             qs = qs = qs.filter(Q(college_name__icontains=query))
                           
         return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')


class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name  = 'program_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program'] = Program.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
         qs = super(ProgramList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None:
             query = self.request.GET.get('q')
             qs = qs = qs.filter(Q(prog_name__icontains=query))
                           
         return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')


class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name  = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
         qs = super(StudentList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None:
             query = self.request.GET.get('q')
             qs = qs = qs.filter(Q(student_id__icontains=query) |
                           Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(program__prog_name__icontains=query))
         return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def BarStudentPerProgram(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT studentorg_program.prog_name AS program_name, COUNT(studentorg_student.id) AS num_students
            FROM studentorg_student
            INNER JOIN studentorg_program ON studentorg_student.program_id = studentorg_program.id
            GROUP BY program_id
        """)
        rows = cursor.fetchall()

    result_with_program_names = {}
    for row in rows:
        program_name = row[0]
        num_students = row[1]
        result_with_program_names[program_name] = num_students

    return JsonResponse(result_with_program_names)

def BarProgramPerCollege(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.college_name, COUNT(p.id) as program_count
               FROM studentorg_program p
               INNER JOIN studentorg_college c ON p.college_id = c.id
               GROUP BY c.college_name
        """)
        rows = cursor.fetchall()

    result_with_program_count = {}
    for row in rows:
        college_name = row[0]
        num_program = row[1]
        result_with_program_count[college_name] = num_program

    return JsonResponse(result_with_program_count)

def PieStudentPerCollege(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.college_name AS college_name, COUNT(s.id) AS num_students
            FROM studentorg_student s
            INNER JOIN studentorg_program p ON s.program_id = p.id
            INNER JOIN studentorg_college c ON p.college_id = c.id
            GROUP BY c.college_name
        """)
        rows = cursor.fetchall()

    result_with_college_names = {}
    for row in rows:
        college_name = row[0]
        num_students = row[1]
        result_with_college_names[college_name] = num_students

    return JsonResponse(result_with_college_names)

def DoughnutOrgPerCollege(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.college_name AS college_name, COUNT(o.id) AS org_count
            FROM studentorg_organization o
            INNER JOIN studentorg_college c ON o.college_id = c.id
            GROUP BY c.college_name
        """)
        rows = cursor.fetchall()

    result_with_org_count = {}
    for row in rows:
        college_name = row[0]
        num_org = row[1]
        result_with_org_count[college_name] = num_org

    return JsonResponse(result_with_org_count)

def RadarMemberPerOrg(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.name, COUNT(om.id) as member_count
            FROM studentorg_orgmember om
            INNER JOIN studentorg_organization o ON om.organization_id = o.id
            GROUP BY o.name
        """)
        rows = cursor.fetchall()

    results = {}
    for row in rows:
        org_name = row[0]
        num_member = row[1]
        results[org_name] = num_member

    return JsonResponse(results)