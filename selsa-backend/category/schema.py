import graphene
from graphene_django.types import DjangoObjectType
from .models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"  # Or list them explicitly for control

    def resolve_parent(self, info):
        return self.parent


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, slug=graphene.String(required=True))

    def resolve_all_categories(root, info):
        return Category.objects.all().order_by("tree_id", "lft")

    def resolve_category(root, info, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None
