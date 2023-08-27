# Generated by Django 4.2.3 on 2023-08-24 01:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_internprofile_email_internprofile_first_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="internprofile",
            name="email",
        ),
        migrations.RemoveField(
            model_name="internprofile",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="internprofile",
            name="last_name",
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
