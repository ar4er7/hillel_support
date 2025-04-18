# Generated by Django 4.2.16 on 2025-03-02 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("issues", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="junior",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="junior_issues",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="senior",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="senior_issues",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
