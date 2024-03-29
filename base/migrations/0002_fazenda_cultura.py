# Generated by Django 4.2 on 2024-03-28 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fazenda",
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
                ("codigo", models.CharField(max_length=15)),
                ("nome_fazenda", models.CharField(max_length=255)),
                ("nome_produtor", models.CharField(max_length=255)),
                ("cidade", models.CharField(max_length=255)),
                ("uf", models.CharField(max_length=2)),
                ("area_total", models.IntegerField()),
                ("area_vegetacao", models.IntegerField()),
                ("area_cultura", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cultura",
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
                    "tipo_cultura",
                    models.CharField(
                        choices=[
                            ("Soja", "Soja"),
                            ("Milho", "Milho"),
                            ("Algodão", "Algodão"),
                            ("Café", "Café"),
                            ("Cana", "Cana"),
                        ],
                        max_length=15,
                    ),
                ),
                ("area", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "fazenda",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="base.fazenda",
                    ),
                ),
            ],
        ),
    ]
