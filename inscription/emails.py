# inscription/emails.py

from django.core.mail import send_mail
from django.conf import settings

def notifier_admission(utilisateur, concours, admis):
    """
    Envoie un mail texte simple après import des résultats.
    AUCUN HTML (safe).
    """

    if not utilisateur.email:
        print("⚠️ UTILISATEUR SANS EMAIL")
        return

    sujet = f"Résultat du concours {concours.nom}"

    if admis:
        message = (
            f"Bonjour {utilisateur.first_name},\n\n"
            f"Félicitations ! Vous êtes ADMIs au concours {concours.nom}.\n\n"
            f"Vous pouvez procéder à votre inscription universitaire.\n\n"
            f"— Service Scolarité"
        )
    else:
        message = (
            f"Bonjour {utilisateur.first_name},\n\n"
            f"Nous sommes désolés de vous informer que vous n'avez pas été admis "
            f"au concours {concours.nom}.\n\n"
            f"— Service Scolarité"
        )

    print("📧 ENVOI MAIL TEXTE...")
    print("➡️ Vers :", utilisateur.email)

    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [utilisateur.email],
        fail_silently=False
    )

    print("✅ MAIL TEXTE ENVOYÉ")
