from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_product_product_features"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="badge_label",
            field=models.CharField(blank=True, default="Sale", max_length=40),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="product",
            name="chair_type",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="product",
            name="hover_image",
            field=models.URLField(blank=True),
        ),
    ]
