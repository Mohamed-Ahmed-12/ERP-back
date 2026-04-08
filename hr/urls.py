from django.urls import path
from rest_framework.routers import DefaultRouter

from hr.views.attendance import AttendanceViewSet
from hr.views.departments import DepartmentViewSet
from hr.views.employee import EmployeeViewset
from hr.views.positions import JobPositionViewSet
from hr.views.vacancy import VacancyViewSet
from hr.views.candidates import CandidateViewSet
from hr.views.job_change_req import JobChangeRequestView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', JobPositionViewSet, basename='jobposition')
router.register(r'employees', EmployeeViewset, basename='employee')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'vacancies', VacancyViewSet, basename='vacancy')
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'job-change-requests', JobChangeRequestView, basename='job-change-req')

urlpatterns = router.urls
