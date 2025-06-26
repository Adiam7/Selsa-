from django import forms
from .models import Category
from mptt.forms import TreeNodeChoiceField


class CategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        required=False,
        level_indicator='— ',
        empty_label="No parent (top level)"
    )

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'description',
            'parent',
            'image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'slug': 'Optional. Leave blank to auto-generate from the name.',
        }
