# Generated by Django 4.2.4 on 2023-08-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Allocation', '0009_cours_etudiant_alter_cours_enseignant'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='sexe',
            field=models.CharField(choices=[('feminin', 'Feminin'), ('masculin', 'Masculin')], default=None, max_length=100),
        ),
    ]