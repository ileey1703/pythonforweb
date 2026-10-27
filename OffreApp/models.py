from decimal import Decimal
from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition


class offre(models.Model):
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.1'))]
    )
    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    statut = models.CharField(
        max_length=100,
        choices=[
            ('p', 'proposee'),
            ('a', 'acceptee'),
            ('r', 'refusee'),
            ('re', 'retiree')
        ],
        default='p'
    )
    date_proposition = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='offres')
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='offres')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='offres')

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 't':
            raise ValidationError("une offre ne peut pas etre faite par un transporteur.")
        if self.vehicule_id and self.vehicule.entreprise_id != self.entreprise_id:
            raise ValidationError("Le véhicule associé à l'offre doit appartenir à la même entreprise que l'offre.")
        if self.expedition_id and self.statut == 'p' and self.expedition.statut != 'publiee':
            raise ValidationError("L'expédition associée à l'offre doit être publiée pour pouvoir recevoir des offres.")
        if self.expedition_id and self.statut == 'a' and self.expedition.statut != 'publiee':
            offre_deja_acceptee = (
                self.pk
                and self.expedition.statut == 'attribuee'
                and offre.objects.filter(pk=self.pk, statut='a').exists()
            )
            if not offre_deja_acceptee:
                raise ValidationError("Seule une expédition publiée peut recevoir une offre acceptée.")
        if self.statut == 'p' and offre.objects.filter(entreprise_id=self.entreprise_id, expedition_id=self.expedition_id, statut='p').exclude(pk=self.pk).exists():
            raise ValidationError("Cette entreprise a déjà une offre proposée pour cette expédition.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)
            if self.statut == 'a' and self.expedition_id:
                expedition = Expedition.objects.select_for_update().get(
                    pk=self.expedition_id
                )
                autres_offres = (
                    offre.objects.select_for_update()
                    .filter(expedition_id=self.expedition_id, statut='p')
                    .exclude(pk=self.pk)
                )
                for autre_offre in autres_offres:
                    autre_offre.statut = 'r'
                    autre_offre.save()
                if expedition.statut == 'publiee':
                    expedition.statut = 'attribuee'
                    expedition.save()
