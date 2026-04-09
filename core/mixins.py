from django.apps import apps


class OptionalFKMixin:
    """
    A mixin that provides a factory method for creating optional cross-module
    foreign key properties without hard imports or DB-level constraints.

    Problem it solves:
        In a modular ERP system, some apps may or may not be installed.
        Using a standard Django ForeignKey to an optional module causes
        ImportError or AppRegistryNotReady if that module is missing.

    Solution:
        Store only the UUID of the related object, and resolve it lazily
        at runtime using Django's app registry — only if the app is installed.

    Usage:
        class Equipment(OptionalFKMixin, models.Model):
            main_driver_id = models.UUIDField(null=True, blank=True)
            main_driver = OptionalFKMixin.optional_fk_property(
                app_label="hr",
                model_name="Employee",
                id_field="main_driver_id",
                pk_field="guid",
            )
    """

    @classmethod
    def optional_fk_property(cls, app_label: str, model_name: str, id_field: str, pk_field: str = "id"):
        """
        Factory method that creates and returns a @property descriptor for
        lazily resolving an optional foreign key relationship at runtime.

        This method is called once at class definition time, not per instance.
        It captures the arguments in a closure and returns a property object
        that performs the actual DB lookup when accessed on an instance.

        Args:
            app_label  (str): The Django app name as registered in INSTALLED_APPS.
                              e.g. "hr", "merchant", "warehouse"

            model_name (str): The model class name inside the target app.
                              e.g. "Employee", "Merchant", "ItemType"

            id_field   (str): The field name on THIS model that stores the
                              target object's UUID.
                              e.g. "main_driver_id", "merchant_id"

            pk_field   (str): The field name on the TARGET model that serves
                              as its primary key. Defaults to "id".
                              Use this when the target model uses a custom PK
                              name like "guid".
                              e.g. "guid", "id"

        Returns:
            property: A descriptor that, when accessed on a model instance,
                      returns the related model instance or None.

        Example:
            # At class definition (runs once):
            main_driver = OptionalFKMixin.optional_fk_property(
                "hr", "Employee", "main_driver_id", pk_field="guid"
            )

            # At runtime (runs on every access):
            equipment.main_driver  →  Employee instance or None
        """

        @property
        def resolver(self):
            """
            The actual property descriptor executed on every attribute access.

            Performs three safety checks before hitting the database:
                1. The UUID field is not null/empty.
                2. The target app is installed in this environment.
                3. The model can be retrieved from the app registry.

            Then executes a dynamic ORM query using the captured closure
            variables and returns the first matching instance or None.

            Args:
                self: The model instance this property is accessed on.
                      e.g. the Equipment instance when accessing
                      equipment.main_driver

            Returns:
                Model instance if found, None otherwise.

            Raises:
                Nothing — all failure cases return None gracefully.
            """

            # Step 1: Get the raw UUID value stored on this instance
            # e.g. equipment.main_driver_id → UUID('abc-123...') or None
            raw_id = getattr(self, id_field)

            # Step 2: If the UUID is null or empty, nothing to resolve
            if not raw_id:
                return None

            # Step 3: Check if the target app is installed in this environment
            # Allows the module to be optional — no crash if "hr" is not installed
            if not apps.is_installed(app_label):
                return None

            # Step 4: Dynamically fetch the model class from the app registry
            # Avoids hard imports like `from hr.models import Employee`
            # which would cause circular imports or ImportError
            Model = apps.get_model(app_label, model_name)

            # Step 5: Query the target model using the custom pk_field
            # **{pk_field: raw_id} dynamically builds e.g. filter(guid=UUID('abc...'))
            return Model.objects.filter(**{pk_field: raw_id}).first()

        return resolver
    
# =======================

from rest_framework.response import Response

class ApiResponseMixin:
    """
    Mixin to standardize all DRF responses to the ERP's custom format.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        # Only wrap data if it hasn't been wrapped already 
        # and if the status code indicates success (2xx)
        if isinstance(response, Response) and 200 <= response.status_code < 300:
            
            # Extract standard DRF pagination if it exists
            pagination = None
            if hasattr(response, 'paginated_data'):
                pagination = response.paginated_data # You'll need to set this in your paginator
            
            custom_body = {
                "success": True,
                "status": response.status_code,
                "message": getattr(self, 'custom_message', "Success."),
                "data": response.data,
            }
            
            if pagination:
                custom_body["pagination"] = pagination
                
            response.data = custom_body
            
        return super().finalize_response(request, response, *args, **kwargs)