from tkinter import *
from tkinter import filedialog  # Ajout de l'import pour filedialog
import requests
from bs4 import BeautifulSoup

# Fonction pour analyser la page web
def analyser_page_web():
    # Récupérer l'URL depuis la saisie
    url = saisie_url.get()

    # Vérifier si l'URL est non vide
    if not url or url == saisie_url.default_text:
        resultat.config(text="Veuillez entrer une URL valide.")
        return

    try:
        # Effectuer la requête HTTP pour récupérer le contenu de la page web
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a réussi

        # Analyser le contenu HTML de la page web
        soup = BeautifulSoup(response.text, 'html.parser')

        # Nombre de liens sortants
        liens_sortants = len(soup.find_all('a', href=True))

        # Nombre de liens internes
        liens_internes = len([link for link in soup.find_all('a', href=True) if link['href'].startswith('/')])

        # % de balises alt sur le nombre d'images
        images = soup.find_all('img')
        balises_alt = sum(1 for img in images if img.get('alt'))

        # Les 3 premières valeurs des mots clés pertinents
        mots_cles = [meta.get('content') for meta in soup.find_all('meta', attrs={'name': 'keywords'})]

        # Les mots clés saisis par l'utilisateur
        mots_cles_utilisateur = saisie_mots_cles.get().split(',')

        # Vérifier si les mots clés de l'utilisateur sont parmi les 3 premiers
        mots_cles_present = any(keyword in mots_cles[:3] for keyword in mots_cles_utilisateur)

        # Afficher les résultats dans l'étiquette résultat
        resultat.config(
            text=f"Liens sortants: {liens_sortants}\nLiens internes: {liens_internes}\n%"
                 f" Balises alt sur le nombre d'images: {balises_alt / len(images) * 100:.2f}%\n"
                 f"Les 3 premiers mots clés pertinents: {', '.join(mots_cles[:3])}\n"
                 f"Mots clés de l'utilisateur parmi les 3 premiers: {'Oui' if mots_cles_present else 'Non'}"
        )

    except requests.RequestException as e:
        resultat.config(text=f"Erreur lors de la requête HTTP : {e}")
    except Exception as e:
        resultat.config(text=f"Une erreur s'est produite : {e}")

# Fonction pour sauvegarder le rapport de référencement
def sauvegarder_rapport():
    rapport = resultat.cget("text")
    if not rapport:
        resultat.config(text="Aucun rapport à sauvegarder.")
        return

    # Utiliser filedialog pour obtenir le chemin du fichier
    fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])

    # Vérifier si l'utilisateur a annulé la boîte de dialogue
    if not fichier:
        return

    with open(fichier, "w") as fichier_sortie:
        fichier_sortie.write(rapport)

    resultat.config(text="Rapport sauvegardé avec succès dans : {}".format(fichier))

# Fonction pour mettre à jour la liste des mots-clés parasites
def mettre_a_jour_mots_parasites():
    # Ajoutez ici le code pour mettre à jour la liste des mots-clés parasites
    resultat.config(text="Liste des mots-clés parasites mise à jour.")

# Fonction pour réinitialiser les champs de saisie
def reinitialiser_champs(event):
    saisie = event.widget
    if saisie.get() == saisie.default_text:
        saisie.delete(0, END)
        saisie.config(fg='black')

# J'importe la bibliothèque graphique TK
fenetre = Tk()

fenetre.title("Première interface")
fenetre.geometry("500x500")

# Création d'un menu
menu_principal = Menu(fenetre)
fenetre.config(menu=menu_principal)

# Création d'un sous-menu "Fichier"
menu_fichier = Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Fichier", menu=menu_fichier)

# Ajout des options dans le sous-menu "Fichier"
menu_fichier.add_command(label="Sauvegarder le rapport", command=sauvegarder_rapport)
menu_fichier.add_command(label="Mettre à jour les mots-clés parasites", command=mettre_a_jour_mots_parasites)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=fenetre.quit)

label = Label(fenetre, text="Entrer l'URL d'une page web :")
label.pack()

# Widget Entry pour la saisie d'une adresse URL
saisie_url = Entry(fenetre, width=35, fg='grey', insertborderwidth=1)
saisie_url.insert(0, "Taper une adresse URL à cette endroit")
saisie_url.default_text = "Taper une adresse URL à cette endroit"
saisie_url.pack()

# Lier la fonction de réinitialisation au clic dans la saisie_url
saisie_url.bind("<FocusIn>", reinitialiser_champs)
saisie_url.bind("<FocusOut>", reinitialiser_champs)

label = Label(fenetre, text="Entrer les mots clés dont vous voulez vous réferencer qui se trouvent sur la page web :")
label.pack()

# Widget Entry pour la saisie des mots clés dont vous voulez vous référencer
saisie_mots_cles = Entry(fenetre, width=60, fg='grey', insertborderwidth=1)
saisie_mots_cles.insert(0, "Taper les mot clés dont vous voulez vous réferencer à cette endroit")
saisie_mots_cles.default_text = "Taper les mot clés dont vous voulez vous réferencer à cette endroit"
saisie_mots_cles.pack()

# Lier la fonction de réinitialisation au clic dans la saisie_mots_cles
saisie_mots_cles.bind("<FocusIn>", reinitialiser_champs)
saisie_mots_cles.bind("<FocusOut>", reinitialiser_champs)

# Widget Bouton pour lancer l'analyse
bouton_analyser = Button(fenetre, text="Analyser la page web", command=analyser_page_web)
bouton_analyser.pack()

# Étiquette pour afficher les résultats
resultat = Label(fenetre, text="")
resultat.pack()

fenetre.mainloop()
