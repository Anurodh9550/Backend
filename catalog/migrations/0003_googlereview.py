from django.db import migrations, models


def seed_google_reviews(apps, schema_editor):
    GoogleReview = apps.get_model("catalog", "GoogleReview")
    if GoogleReview.objects.exists():
        return
    GoogleReview.objects.bulk_create(
        [
            GoogleReview(
                name="Sonu Prasad",
                review_text=(
                    "Writing this review after using the chair for 10 days. "
                    "Robocura's Serene has helped me relax and smoothen my muscles."
                ),
                rating=5,
                source_label="Google",
                reviewed_at="2023-01-10",
                display_order=1,
            ),
            GoogleReview(
                name="Kailash Babu",
                review_text="Nice products.",
                rating=5,
                source_label="Google",
                reviewed_at="2020-08-20",
                display_order=2,
            ),
            GoogleReview(
                name="Sadaf Chaudhry",
                review_text="Tried in GIP Mall Noida. Amazing experience.",
                rating=5,
                source_label="Google",
                reviewed_at="2020-05-12",
                display_order=3,
            ),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_contactsubmission_warrantyclaim_product_image_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoogleReview",
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
                ("name", models.CharField(max_length=160)),
                ("review_text", models.TextField()),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("source_label", models.CharField(default="Google", max_length=80)),
                ("source_url", models.URLField(blank=True)),
                ("reviewed_at", models.DateField(blank=True, null=True)),
                ("is_featured", models.BooleanField(default=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["display_order", "-created_at"],
            },
        ),
        migrations.RunPython(seed_google_reviews, migrations.RunPython.noop),
    ]
