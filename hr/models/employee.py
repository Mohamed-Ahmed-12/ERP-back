 
from django.db import models
from core.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeDocumentTypeChoices(models.TextChoices):
    CONTRACT = 'Contract', 'Contract'
    ID_PROOF = 'ID Proof', 'ID Proof'
    ADDRESS_PROOF = 'Address Proof', 'Address Proof'
    OTHER = 'Other', 'Other'

class GenderChoices(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'

class MaritalStatusChoices(models.TextChoices):
    SINGLE = 'Single', 'Single'
    MARRIED = 'Married', 'Married'
    DIVORCED = 'Divorced', 'Divorced'
    WIDOWED = 'Widowed', 'Widowed'
    
class MilitaryStatusChoices(models.TextChoices):
    COMPLETED = 'Completed', 'Completed'
    EXEMPTED = 'Exempted', 'Exempted'
    NOT_COMPLETED = 'Not Completed', 'Not Completed'

class EducationLevelChoices(models.TextChoices):
    HIGH_SCHOOL = 'High School', 'High School'
    ASSOCIATE_DEGREE = 'Associate Degree', 'Associate Degree'
    BACHELORS_DEGREE = "Bachelor's Degree", "Bachelor's Degree"
    MASTERS_DEGREE = "Master's Degree", "Master's Degree"
    DOCTORATE = 'Doctorate', 'Doctorate'
    OTHER = 'Other', 'Other'
    
    
class Employee(BaseModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255,blank=True, null=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True, null=True , choices=GenderChoices.choices)
    dob = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True , choices=MaritalStatusChoices.choices)
    military_status = models.CharField(max_length=20, blank=True, null=True , choices=MilitaryStatusChoices.choices)   
    education_level = models.CharField(max_length=50, blank=True, null=True , choices=EducationLevelChoices.choices)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    position = models.ForeignKey('JobPosition', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    date_hired = models.DateField(null=True, blank=True)
    work_email = models.EmailField(unique=True, blank=True, null=True)
    
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    id_front = models.ImageField(upload_to='employee_ids/', null=True, blank=True)
    id_back = models.ImageField(upload_to='employee_ids/', null=True, blank=True)
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)    
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    is_active = models.BooleanField(default=True)
    contract_end_date = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        app_label = 'hr'
    
    @property
    def current_salary(self):
        if self.position:
            return self.position.base_salary
        return 0  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeDocument(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, blank=True, null=True , choices=EmployeeDocumentTypeChoices.choices)
    document_file = models.FileField(upload_to='employee_documents/')
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'
        app_label = 'hr'
    def __str__(self):
        return f"{self.document_type} for {self.employee.first_name} {self.employee.last_name}"
