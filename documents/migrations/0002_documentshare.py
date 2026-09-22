from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentShare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("viewer", "Viewer"), ("editor", "Editor")],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shares",
                        to="documents.document",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_shares",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="documentshare",
            constraint=models.UniqueConstraint(
                fields=("document", "user"),
                name="unique_document_share_user",
            ),
        ),
        migrations.AddConstraint(
            model_name="documentshare",
            constraint=models.CheckConstraint(
                condition=models.Q(role__in=["viewer", "editor"]),
                name="valid_document_share_role",
            ),
        ),
        migrations.AddIndex(
            model_name="documentshare",
            index=models.Index(
                fields=["user", "document"],
                name="documents_d_user_id_6410f1_idx",
            ),
        ),
    ]
