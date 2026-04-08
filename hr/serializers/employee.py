
from rest_framework import serializers
from hr.models.employee import Employee
from hr.serializers.departments import DepartmentSerializer
from hr.serializers.positions import JobPositionReadSerializer 


class EmployeeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['guid', 'first_name', 'last_name' , 'email']

        
class EmployeeSerializer(serializers.ModelSerializer):
    position = JobPositionReadSerializer(read_only=True) 
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            # Personal Identity
            'first_name', 'middle_name', 'last_name', 'gender', 'dob',
            'national_id', 'marital_status', 'military_status', 'education_level',
            
            # Contact & Location
            'phone_number', 'email', 'work_email', 'address', 'city', 'country',
            
            # Work & Hierarchy
            'position', 'department', 'manager', 'date_hired', 'contract_end_date',
            'is_active', 'user',
            
            # Files/Images (Handled via Multipart/Form-Data)
            'photo', 'id_front', 'id_back'
        ]

    def validate_email(self, value):
        """Normalize email to lowercase for consistency."""
        return value.lower()

    def validate(self, data):
        """
        Cross-field validation.
        """
        manager = data.get('manager')
        
        # 1. Prevent an employee from being their own manager
        if self.instance and manager and self.instance.pk == manager.pk:
            raise serializers.ValidationError({
                "manager": "An employee cannot be their own manager."
            })
            
        # 2. Basic Date check: Hired date vs Contract end
        date_hired = data.get('date_hired') or (self.instance.date_hired if self.instance else None)
        contract_end = data.get('contract_end_date') or (self.instance.contract_end_date if self.instance else None)
        
        if date_hired and contract_end and contract_end <= date_hired:
            raise serializers.ValidationError({
                "contract_end_date": "Contract end date must be after the hiring date."
            })

        return data