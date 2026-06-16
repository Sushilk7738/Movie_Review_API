from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Movie


@receiver(post_save, sender = Movie)
def generate_slug(sender, instance, created, **kwargs):
    if created:
        Movie.objects.filter(
            pk = instance.pk
        ).update(
            slug = slugify(instance.title)
        )
