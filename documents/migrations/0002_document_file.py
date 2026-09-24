from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("documents", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="document",
            name="file",
            field=models.FileField(blank=True, upload_to="documents/%Y/%m/%d/"),
        ),
    ]
