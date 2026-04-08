from __future__ import annotations

import uuid
from typing import TypeVar

from django.db import models
from django.utils import timezone

_M = TypeVar("_M", bound="BaseModel")

class SoftDeleteQuerySet(models.QuerySet[_M]):
    def delete(self):
        # This handles bulk deletes: Department.objects.filter(...).delete()
        return super().update(is_deleted=True, deleted_at=timezone.now())

class SoftDeleteManager(models.Manager[_M]):
    """Default manager — transparently excludes soft-deleted records."""

    def get_queryset(self) -> SoftDeleteQuerySet[_M]:  # type: ignore[override]
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def with_deleted(self) -> SoftDeleteQuerySet[_M]:
        """Return a queryset that includes soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db)
    


class AllObjectsManager(models.Manager[_M]):  # type: ignore[type-arg]
    """Unfiltered manager — use sparingly for admin / data-repair tasks."""

    pass


class BaseModel(models.Model):
    """Abstract base for every model in the platform.

    Provides:
    - UUID primary key
    - Automatic created_at / updated_at timestamps
    - Soft-delete with restore support
    - ``objects`` manager that hides deleted rows by default
    - ``all_objects`` manager that returns everything
    - ``objects.with_deleted()`` escape hatch
    """

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Mark the record as deleted without removing it from the database."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def restore(self) -> None:
        """Undo a soft delete."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
