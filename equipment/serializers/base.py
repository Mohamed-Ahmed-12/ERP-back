from rest_framework import serializers
from django.apps import apps

from equipment.models import Equipment , EquipmentType , EquipmentBrand , EquipmentEmployee

# ===== Equipment Employee =====

class EquipmentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentEmployee
        fields = ["guid" , "first_name" , "last_name", "national_id" , "phone_number" , "employee_id" , "source"]
        read_only_fields = ['guid' , 'source','employee_id']

# ===== Equipment Type =====

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model =EquipmentType
        fields = ['guid' , 'drivable' , 'name']
        read_only_fields = ['guid']

# ===== Equipment Brand =====

class EquipmentBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model =EquipmentBrand
        fields = ['guid' , 'name']
        read_only_fields = ['guid']


# ===== Equipment =====

class EquipmentReadSerializer(serializers.ModelSerializer):
    """
    Read serializer for Equipment model.
    Resolves all FK fields into nested representations.
    main_driver and sub_driver now point to local Driver model
    instead of hr.Employee directly.
    """

    equipment_type  = serializers.SerializerMethodField()
    equipment_brand = serializers.SerializerMethodField()
    main_driver     = serializers.SerializerMethodField()
    sub_driver      = serializers.SerializerMethodField()
    status_display  = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Equipment
        fields = [
            "guid",
            "serial_number",
            "name",
            "model",
            "status",
            "status_display",
            "equipment_type",
            "equipment_brand",
            # Driver FK ids (for form pre-population)
            "main_driver_id",
            "main_driver",
            "sub_driver_id",
            "sub_driver",
            "created_at",
            "updated_at",
        ]

    def get_equipment_type(self, obj):
        if not obj.equipment_type:
            return None
        return {
            "guid":     obj.equipment_type.guid,
            "name":     obj.equipment_type.name,
            "drivable": obj.equipment_type.drivable,
        }

    def get_equipment_brand(self, obj):
        if not obj.equipment_brand:
            return None
        return {
            "guid": obj.equipment_brand.guid,
            "name": obj.equipment_brand.name,
        }

    def _serialize_driver(self, driver):
        """
        Serialize a local Driver instance.
        Returns source field so frontend knows
        whether this driver is synced from HR or entered locally.
        """
        if not driver:
            return None
        return EquipmentEmployeeSerializer(driver).data

    def get_main_driver(self, obj):
        return self._serialize_driver(obj.main_driver)

    def get_sub_driver(self, obj):
        return self._serialize_driver(obj.sub_driver)



class EquipmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = [
            "serial_number",
            "name",
            "model",
            "status",
            "equipment_type",
            "equipment_brand",
            "main_driver",
            "sub_driver",
        ]
    # -----------------------------
    # CROSS VALIDATION
    # -----------------------------
    def validate(self, attrs):
        main = attrs.get("main_driver")
        sub = attrs.get("sub_driver")

        if main and sub and main.guid == sub.guid:
            raise serializers.ValidationError({
                "sub_driver": "Main driver and sub driver cannot be the same person."
            })

        return attrs

    def to_representation(self, instance):
        return EquipmentReadSerializer(
            instance,
            context=self.context
        ).data