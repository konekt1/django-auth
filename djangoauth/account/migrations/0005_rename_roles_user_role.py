# Generated by Django 4.2.3 on 2023-08-24 01:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_remove_internprofile_email_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="roles",
            new_name="role",
        ),
    ]