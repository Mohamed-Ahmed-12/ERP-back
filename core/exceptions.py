
from __future__ import annotations

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import Http404

from rest_framework import exceptions as drf_exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Shape builder
# ──────────────────────────────────────────────

def _error_response(
    status: int,
    code: str,
    message: str,
    details=None,
) -> Response:
    body = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "status": status,
    }
    return Response(body, status=status)


# ──────────────────────────────────────────────
# Details normalizer
# ──────────────────────────────────────────────

def _normalize_details(detail):
    """
    Recursively converts DRF ErrorDetail / dicts / lists 
    into plain Python strings so the response is JSON-clean.
    """
    if isinstance(detail, list):
        return [_normalize_details(item) for item in detail]
    if isinstance(detail, dict):
        return {key: _normalize_details(val) for key, val in detail.items()}
    return str(detail)


# ──────────────────────────────────────────────
# Map Django → DRF exceptions (runs first)
# ──────────────────────────────────────────────

def _convert_django_exceptions(exc):
    if isinstance(exc, Http404):
        return drf_exceptions.NotFound()

    if isinstance(exc, DjangoPermissionDenied):
        return drf_exceptions.PermissionDenied()

    if isinstance(exc, DjangoValidationError):
        return ValidationError(detail=exc.message_dict if hasattr(exc, "message_dict") else exc.messages)

    if isinstance(exc, ObjectDoesNotExist):
        return drf_exceptions.NotFound(detail=str(exc))

    if isinstance(exc, IntegrityError):
        # e.g. unique constraint, FK violation
        return drf_exceptions.ValidationError(
            detail={"non_field_errors": ["A record with this data already exists."]},
            code="integrity_error",
        )

    return None  # Not a Django exception we handle


# ──────────────────────────────────────────────
# Custom codes per DRF exception class
# ──────────────────────────────────────────────

EXCEPTION_CODE_MAP: dict[type, str] = {
    drf_exceptions.ValidationError:        "validation_error",
    drf_exceptions.AuthenticationFailed:   "authentication_failed",
    drf_exceptions.NotAuthenticated:       "not_authenticated",
    drf_exceptions.PermissionDenied:       "permission_denied",
    drf_exceptions.NotFound:               "not_found",
    drf_exceptions.MethodNotAllowed:       "method_not_allowed",
    drf_exceptions.NotAcceptable:          "not_acceptable",
    drf_exceptions.UnsupportedMediaType:   "unsupported_media_type",
    drf_exceptions.Throttled:              "throttled",
}


# ──────────────────────────────────────────────
# Main handler — wire this up in settings.py
# ──────────────────────────────────────────────

def custom_exception_handler(exc, context):
    # Step 1 — Try to convert Django exceptions to DRF ones
    converted = _convert_django_exceptions(exc)
    if converted:
        exc = converted

    # Step 2 — Let DRF handle its own exceptions (sets exc.status_code)
    response = drf_exception_handler(exc, context)

    # Step 3 — DRF returned a response: reformat it
    if response is not None:
        detail = exc.detail if hasattr(exc, "detail") else str(exc)
        details = _normalize_details(detail)

        # For non-validation errors the detail IS the message; no extra details needed
        if isinstance(exc, drf_exceptions.ValidationError):
            message = "Invalid input. Please check the submitted data."
        else:
            # Flatten single-string details into message directly
            message = details if isinstance(details, str) else "An error occurred."
            details = None

        code = EXCEPTION_CODE_MAP.get(type(exc), getattr(exc, "default_code", "error"))
        return _error_response(response.status_code, code, message, details)

    # Step 4 — Unhandled exception (500)
    logger.exception(
        "Unhandled exception in view %s",
        context.get("view").__class__.__name__ if context.get("view") else "unknown",
        exc_info=exc,
    )
    return _error_response(
        status=500,
        code="internal_server_error",
        message="An unexpected error occurred. Please try again later.",
        details=None,
    )