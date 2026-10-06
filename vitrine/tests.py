from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from vitrine.views import index, a_propos, mentions_legales
from actualites.views import index as actualites_index, detail as actualites_detail
from conception.views import index as conception_index, plans_3d, etude_conseil, devis
from realisations.views import index as realisations_index, methode, detail as realisations_detail
from gestion.views import index as gestion_index, acd, locative, louer, vendre, detail_bien
from materiaux.views import index as materiaux_index, materiaux, equipements, engins
from contact.views import index as contact_index

from realisations.models import Realisation
from actualites.models import Article, StatutArticle
from gestion.models import Bien, TypeBienGestion, Transaction, StatutBien
from materiaux.models import CategorieProduit, Produit, TypeOffre


class HabitatDirectViewsTestCase(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.realisation = Realisation.objects.create(
            titre="Villa Test",
            slug="villa-test",
            type_bien="villa",
            ville="Abidjan",
            superficie_m2=200,
            duree_mois=6,
            annee_livraison=2025,
            en_avant=True,
        )
        self.article = Article.objects.create(
            titre="Article Test",
            slug="article-test",
            extrait="Extrait de test",
            contenu="Contenu complet de test",
            statut=StatutArticle.PUBLIE,
        )
        self.bien = Bien.objects.create(
            titre="Bien Test",
            type_bien=TypeBienGestion.VILLA,
            transaction=Transaction.LOUER,
            ville="Cocody",
            prix=500000,
            superficie_m2=150,
            statut=StatutBien.DISPONIBLE,
        )
        self.categorie = CategorieProduit.objects.create(nom="Gros oeuvre")
        self.produit = Produit.objects.create(
            nom="Ciment",
            categorie=self.categorie,
            type_offre=TypeOffre.VENTE,
            prix_indicatif="4500 F",
        )

    def _setup_request_middleware(self, request):
        session_mw = SessionMiddleware(lambda req: None)
        session_mw.process_request(request)
        request.session.save()
        messages_mw = MessageMiddleware(lambda req: None)
        messages_mw.process_request(request)
        return request

    def test_direct_view_executions(self):
        views_to_test = [
            (index, '/'),
            (a_propos, '/a-propos/'),
            (mentions_legales, '/mentions-legales/'),
            (conception_index, '/conception/'),
            (plans_3d, '/conception/plans-3d/'),
            (etude_conseil, '/conception/etude-conseil/'),
            (devis, '/conception/devis/'),
            (realisations_index, '/realisations/'),
            (methode, '/realisations/methode/'),
            (lambda req: realisations_detail(req, slug=self.realisation.slug), f'/realisations/{self.realisation.slug}/'),
            (gestion_index, '/gestion/'),
            (acd, '/gestion/acd/'),
            (locative, '/gestion/locative/'),
            (louer, '/gestion/louer/'),
            (vendre, '/gestion/vendre/'),
            (lambda req: detail_bien(req, pk=self.bien.pk), f'/gestion/bien/{self.bien.pk}/'),
            (materiaux_index, '/import-export/'),
            (materiaux, '/import-export/materiaux/'),
            (equipements, '/import-export/equipements/'),
            (engins, '/import-export/engins/'),
            (actualites_index, '/actualites/'),
            (lambda req: actualites_detail(req, slug=self.article.slug), f'/actualites/{self.article.slug}/'),
            (contact_index, '/contact/'),
        ]

        for view_func, path in views_to_test:
            request = self.rf.get(path)
            response = view_func(request)
            self.assertEqual(response.status_code, 200, f"Failed execution for view at {path}")

    def test_contact_post_execution(self):
        request = self.rf.post('/contact/', {
            'nom_complet': 'Jean Dupont',
            'telephone': '+2250102030405',
            'email': 'jean@example.com',
            'sujet': 'autre',
            'message': 'Message test',
        })
        self._setup_request_middleware(request)
        response = contact_index(request)
        self.assertEqual(response.status_code, 302)

    def test_conception_post_execution(self):
        request = self.rf.post('/conception/', {
            'nom_complet': 'Marie Kouassi',
            'telephone': '+2250708091011',
            'email': 'marie@example.com',
            'ville_terrain': 'Bingerville',
            'superficie_terrain': '500m2',
            'type_projet': 'villa',
            'message': 'Etude villa',
        })
        self._setup_request_middleware(request)
        response = conception_index(request)
        self.assertEqual(response.status_code, 302)

    def test_gestion_post_execution(self):
        request = self.rf.post('/gestion/', {
            'nom_complet': 'Paul Yao',
            'telephone': '+2250506070809',
            'email': 'paul@example.com',
            'type_bien': 'villa',
            'objectif': 'louer',
            'adresse_bien': 'Cocody Angre',
            'message': 'Bien en gestion',
        })
        self._setup_request_middleware(request)
        response = gestion_index(request)
        self.assertEqual(response.status_code, 302)

    def test_materiaux_post_execution(self):
        request = self.rf.post('/import-export/', {
            'nom_entreprise': 'BTP Sarl',
            'telephone': '+2250102030405',
            'produits_recherches': 'Ciment',
            'quantite_estimee': '100 sacs',
            'ville_livraison': 'Abidjan',
        })
        self._setup_request_middleware(request)
        response = materiaux_index(request)
        self.assertEqual(response.status_code, 302)
