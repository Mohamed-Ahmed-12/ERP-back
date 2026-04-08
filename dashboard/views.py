from rest_framework import views
from rest_framework.response import Response 
from hr.models.department import Department
from hr.models.employee import Employee

class DashboardView(views.APIView):
    def get(self , request):
        department_count = Department.objects.count()
        employee_count = Employee.objects.count()
        
        data = {
            'department_count': department_count,
            'employee_count':employee_count
        }
        return Response(data=data)