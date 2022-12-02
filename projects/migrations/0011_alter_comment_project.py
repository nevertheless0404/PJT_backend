# Generated by Django 4.1.3 on 2022-12-02 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0010_remove_comment_parent_remove_comment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="projects.todo",
            ),
        ),
    ]
