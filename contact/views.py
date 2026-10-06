from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MessageContact, SujetContact


def index(request):
    """Page de contact générale avec routage par pôle."""
    if request.method == 'POST':
        nom_complet = request.POST.get('nom_complet', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        sujet = request.POST.get('sujet', SujetContact.AUTRE)
        message = request.POST.get('message', '').strip()

        if nom_complet and telephone and email and message:
            MessageContact.objects.create(
                nom_complet=nom_complet,
                telephone=telephone,
                email=email,
                sujet=sujet,
                message=message,
            )
            messages.success(request, "Merci pour votre message ! Notre équipe étudie votre demande et vous répondra sous 72h.")
            return redirect('contact:index')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires (nom, téléphone, email et message).")

    context = {
        'active_nav': 'contact',
        'sujets': SujetContact.choices,
    }
    return render(request, 'contact.html', context)
