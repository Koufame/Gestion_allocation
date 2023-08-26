# Generated by Django 4.2.4 on 2023-08-21 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Allocation', '0006_delete_projetarchive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='statut',
            field=models.CharField(choices=[('en_cours', 'En cours'), ('soumis', 'Soumis'), ('corrigé', 'Corrigé'), ('traite', 'Traité'), ('archive', 'A0rchivé')], max_length=20),
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('enseignant', models.ForeignKey(limit_choices_to={'role': 'enseignant'}, on_delete=django.db.models.deletion.CASCADE, to='Allocation.utilisateur')),
            ],
        ),
    ]
