from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Utilisateur
from .models import Tache
from .models import Utilisateur
from .models import Cours, Soumission, NoteTravail
from .forms import SoumissionForm
from .forms import CoursForm ,NoteTravailForm

def inscription(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        numero_utilisateur = request.POST['numero_utilisateur']

        # Vérifier si un utilisateur avec le même nom et numéro existe déjà
        if Utilisateur.objects.filter(nom=nom, numero_utilisateur=numero_utilisateur).exists():
            message = "Un utilisateur avec le même nom et numéro existe déjà."
            return render(request, 'inscription.html', {'message': message})

        # Récupérer d'autres données du formulaire
        sexe = request.POST['sexe']
        prenom = request.POST['prenom']
        date_naissance = request.POST['date_naissance']
        role = request.POST['role']
        # Créer un nouvel utilisateur
        utilisateur = Utilisateur(nom=nom,sexe=sexe, prenom=prenom, date_naissance=date_naissance, role=role, numero_utilisateur=numero_utilisateur)
        utilisateur.save()

        return redirect('connexion')  # Rediriger vers la page de connexion après l'inscription
    else:
        return render(request, 'inscription.html')



from django.contrib import messages
def connexion(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire de connexion
        nom = request.POST['nom']
        numero_utilisateur = request.POST['numero_utilisateur']

        try:
            # Vérifier les informations d'identification de l'utilisateur
            utilisateur = Utilisateur.objects.get(nom=nom, numero_utilisateur=numero_utilisateur)

            # Connecter l'utilisateur
            auth.login(request, utilisateur)
            return redirect('cours')
        except Utilisateur.DoesNotExist:
            message = "Identifiant ou mot de passe incorrect."
            messages.error(request, message)
            return render(request, 'connexion.html',{'message': message})
    else:
        return render(request, 'connexion.html')


    

def autoriser_tache(request):
    if request.method == 'POST':
        etudiant = request.POST['etudiant']
        # Récupérer l'étudiant correspondant à l'ID
        etudiant = Utilisateur.objects.get(id=etudiant)
        titre = request.POST['titre']
        matiere = request.POST['matiere']
        fichier = request.FILES['fichier']
        statut = request.POST['statut']

        # Créer une nouvelle instance de Tache avec l'étudiant assigné
        tache = Tache(etudiant=etudiant, titre=titre, matiere=matiere, fichier=fichier, statut= statut)
        tache.save()

        return redirect('liste_taches')
    else:
        # Récupérer tous les étudiants pour les afficher dans le formulaire
        etudiants = Utilisateur.objects.all().filter(role='etudiant')
        return render(request, 'autoriser_tache.html', {'etudiants': etudiants})
    
def liste_taches(request):
    taches = Tache.objects.all()
    return render(request, 'liste_taches.html', {'taches': taches})

def liste_taches_archivees(request):
    taches_archivees = Tache.objects.filter(statut='archivé')
    return render(request, 'archive/liste_taches_archivees.html', {'taches_archivees': taches_archivees})

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Tache

def telecharger_fichier(request, tache_id):
    tache = get_object_or_404(Tache, pk=tache_id)
    fichier = tache.fichier  # Supposons que vous avez un champ FileField nommé "fichier" dans le modèle Tache

    # Générez une réponse de fichier avec le contenu du fichier
    response = FileResponse(fichier)

    # Définissez les en-têtes de la réponse pour spécifier le nom du fichier et le type de contenu
    response['Content-Disposition'] = f'attachment; filename="{fichier.name}"'
    response['Content-Type'] = 'application/octet-stream'  # Utilisez le type de contenu approprié pour votre fichier

    return response

def cours(request):
    cours_en_cours = Cours.objects.all()  # Récupérer tous les cours en cours
     
    context = {
        'cours_en_cours': cours_en_cours,
        'utilisateur': request.user,  # Ajoutez l'utilisateur connecté dans le contexte
    }
    
    return render(request, 'cours.html', context)

def details_cours(request, cours_id):
    cours = get_object_or_404(Cours, pk=cours_id)  # Récupérer le cours par son ID
    return render(request, 'details_cours.html', {'cours': cours})

def mise_a_jour_profil(request):
    utilisateur = request.user  # Récupérer l'utilisateur connecté
    if request.method == 'POST':
        utilisateur.nom = request.POST.get('nom')
        utilisateur.prenom = request.POST.get('prenom')
        # Mettez à jour d'autres champs de profil
        utilisateur.save()
        return redirect('cours')

    return render(request, 'maj_profil.html', {'utilisateur': utilisateur})


def creer_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save(commit=False)
            # cours.enseignant = request.user
            cours.save()
            form.save_m2m() 
            return redirect('cours')  # Rediriger vers la liste des cours

    else:
        form = CoursForm()

    return render(request, 'creer_cours.html', {'form': form})

def soumettre_travail(request, cours_id):
    cours = Cours.objects.get(pk=cours_id)
    
    if request.method == 'POST':
        form = SoumissionForm(request.POST, request.FILES)
        if form.is_valid():
            soumission = form.save(commit=False)
            soumission.etudiant = request.user
            soumission.cours = cours
            soumission.save()
            return redirect('details_cours', cours_id=cours_id)

    else:
        form = SoumissionForm()

    return render(request, 'soumission_travail.html', {'form': form, 'cours': cours})

def autoriser_et_noter_soumission(request, soumission_id):
    soumission = Soumission.objects.get(pk=soumission_id)
    note_travail, created = NoteTravail.objects.get_or_create(soumission=soumission)

    if request.method == 'POST':
        form = NoteTravailForm(request.POST, instance=note_travail)

        if form.is_valid():
            form.save()
            return redirect('details_cours', cours_id=soumission.cours.id)

    else:
        form = NoteTravailForm(instance=note_travail)

    return render(request, 'autorisation_note.html', {'form': form, 'soumission': soumission})

from django.http import HttpResponse
# Vue pour télécharger le fichier
def telecharger_fichier(request, soumission_id):
    soumission = Soumission.objects.get(pk=soumission_id)
    # Ouvrir le fichier en mode binaire
    with soumission.fichier.open('rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{soumission.fichier.name}"'
        return response