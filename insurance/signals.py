from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Risk


@receiver(post_save, sender=Risk)
def create_risk_model(sender, instance, created, **kwargs):
    print("ADD", instance.fields.all())


@receiver(post_delete, sender=Risk)
def delete_risk_model(sender, instance, created, **kwargs):
    print("DEL", instance.fields.all())
