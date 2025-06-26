from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Category


def generate_unique_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.name)
    qs = Category.objects.filter(slug=slug).exclude(pk=instance.pk)
    counter = 1
    while qs.exists():
        slug = f"{slugify(instance.name)}-{counter}"
        qs = Category.objects.filter(slug=slug).exclude(pk=instance.pk)
        counter += 1
    return slug


@receiver(pre_save, sender=Category)
def pre_save_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)


@receiver(post_save, sender=Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print(f"[Category Created] → {instance.name} (slug: {instance.slug})")
    else:
        print(f"[Category Updated] → {instance.name}")


@receiver(post_delete, sender=Category)
def post_delete_category(sender, instance, **kwargs):
    print(f"[Category Deleted] → {instance.name}")
