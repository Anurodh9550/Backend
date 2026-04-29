from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_supportrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="home_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="show_on_home",
            field=models.BooleanField(default=False),
        ),
    ]
