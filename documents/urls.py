from django.urls import path

from . import views

urlpatterns = [
    path("documents/", views.documents, name="documents"),
    path("documents/<int:document_id>/", views.document_detail, name="document-detail"),
    path("admin/documents/", views.admin_documents, name="admin-documents"),
]
