from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0005_product_show_on_home_product_home_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="product_features",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
