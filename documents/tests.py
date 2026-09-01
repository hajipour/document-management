import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Document


class DocumentAuthorizationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.alice = user_model.objects.create_user("alice", password="password")
        self.bob = user_model.objects.create_user("bob", password="password")
        self.document = Document.objects.create(
            owner=self.alice, title="Alice's document", content="private"
        )

    def test_document_detail_cannot_be_read_by_another_user(self):
        self.client.force_login(self.bob)

        response = self.client.get(
            reverse("document-detail", args=[self.document.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_document_is_created_for_authenticated_user_not_payload_owner(self):
        self.client.force_login(self.alice)

        response = self.client.post(
            reverse("documents"),
            data=json.dumps({"title": "New", "content": "text", "owner_id": self.bob.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["owner_id"], self.alice.id)

    def test_admin_endpoint_requires_staff_user(self):
        self.client.force_login(self.alice)
        self.assertEqual(self.client.get(reverse("admin-documents")).status_code, 403)

        self.alice.is_staff = True
        self.alice.save(update_fields=["is_staff"])
        self.assertEqual(self.client.get(reverse("admin-documents")).status_code, 200)
