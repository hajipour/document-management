import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .auth import admin_required, get_current_user
from .models import Document


def _payload(request: HttpRequest) -> dict:
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return {}


def _serialize(document: Document) -> dict:
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "owner_id": document.owner_id,
        "created_at": document.created_at.isoformat(),
        "updated_at": document.updated_at.isoformat(),
    }


@require_http_methods(["GET", "POST"])
def documents(request: HttpRequest) -> JsonResponse:
    current_user = get_current_user(request)
    if request.method == "GET":
        # A user can list only documents they own.
        items = Document.objects.filter(owner_id=current_user.id).order_by("id")
        return JsonResponse({"documents": [_serialize(item) for item in items]})

    data = _payload(request)
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return JsonResponse({"detail": "title is required"}, status=400)
    document = Document.objects.create(
        owner_id=current_user.id,
        title=title.strip(),
        content=data.get("content", ""),
    )
    return JsonResponse(_serialize(document), status=201)


@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def document_detail(request: HttpRequest, document_id: int) -> JsonResponse:
    current_user = get_current_user(request)
    # Never look up a document by ID alone: this enforces object-level ownership.
    document = get_object_or_404(
        Document, id=document_id, owner_id=current_user.id
    )

    if request.method == "GET":
        return JsonResponse(_serialize(document))
    if request.method == "DELETE":
        document.delete()
        return JsonResponse({}, status=204)

    data = _payload(request)
    for field in ("title", "content"):
        if field in data:
            setattr(document, field, data[field])
    if not isinstance(document.title, str) or not document.title.strip():
        return JsonResponse({"detail": "title must not be blank"}, status=400)
    if not isinstance(document.content, str):
        return JsonResponse({"detail": "content must be a string"}, status=400)
    document.title = document.title.strip()
    document.save(update_fields=["title", "content", "updated_at"])
    return JsonResponse(_serialize(document))


@admin_required
@require_http_methods(["GET"])
def admin_documents(request: HttpRequest) -> JsonResponse:
    """Application admin route, protected by the is_admin dependency."""
    items = Document.objects.select_related("owner").order_by("id")
    return JsonResponse({"documents": [_serialize(item) for item in items]})
