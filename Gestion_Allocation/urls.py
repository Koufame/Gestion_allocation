"""Gestion_Allocation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Allocation import views

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('autoriser-tache/', views.autoriser_tache, name='autoriser_tache'),
    path('liste-taches/', views.liste_taches, name='liste_taches'),
    path('taches/archivees/', views.liste_taches_archivees, name='liste_taches_archivees'),
    path('tache/<int:tache_id>/telecharger/', views.telecharger_fichier, name='telecharger_fichier'),
    path('creer_cours/', views.creer_cours, name='creer_cours'),
    path('cours/', views.cours, name='cours'),
    path('cours/<int:cours_id>/', views.details_cours, name='details_cours'),
    path('profil/mise_a_jour/', views.mise_a_jour_profil, name='mise_a_jour_profil'),
    path('soumettre-travail/<int:cours_id>/', views.soumettre_travail, name='soumettre_travail'),
    path('autoriser_et_noter_soumission/<int:soumission_id>/', views.autoriser_et_noter_soumission, name='autoriser_et_noter_soumission'),
    path('telecharger_fichier/<int:soumission_id>/', views.telecharger_fichier, name='telecharger_fichier'),

]