# Generated by Django 4.0.1 on 2022-01-23 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Qsee', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Analysers',
            new_name='Analyser',
        ),
        migrations.RenameModel(
            old_name='Assays',
            new_name='Assay',
        ),
        migrations.RenameModel(
            old_name='Controls',
            new_name='Control',
        ),
        migrations.RenameModel(
            old_name='Tests',
            new_name='Test',
        ),
    ]
