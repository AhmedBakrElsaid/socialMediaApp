# Generated by Django 4.2.5 on 2023-12-28 11:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userauth", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="profiling",
            new_name="profileimg",
        ),
    ]