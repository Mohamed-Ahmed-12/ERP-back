from django.contrib import admin

from .models.employee import Employee
from .models.department import Department
from .models.job_position import JobPosition
from .models.vacation import VacationBalance
from .models.job_change_request import JobChangeRequest
from .models.attendance import Attendance
from .models.candidate import Candidate 
from .models.vacancy import Vacancy

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(JobPosition)
admin.site.register(Vacancy)
admin.site.register(Attendance)
admin.site.register(Candidate)
