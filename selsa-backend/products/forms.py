from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
import importlib
from .models import (Product, ProductImage, ProductVariant, ProductReview, 
                     ProductOptionValue, ProductOptionType)
#ProductOption,

# Custom MultiFile Input Field
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Enables multiple file selection

# Custom MultiFile Field to handle multiple file uploads
class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        """Convert input data to a list of files."""
        if not data:
            return []
        if not isinstance(data, list):  # Ensure it's always a list
            return [data]
        return data


# Product Form for creating/updating products
class ProductForm(forms.ModelForm):
    images = MultiFileField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'description']  # Exclude image from here
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        """Override save method to handle image upload."""
        product = super().save(commit=False)
        if commit:
            product.save()

            # Save multiple images
            images = self.cleaned_data.get('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)

        return product



# Product Image Upload Form for adding product images
class ProductImageUploadForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary'] # Assuming 'image' is the field in the ProductImage model

# Custom form to handle multiple images
ProductImageFormSet = modelformset_factory(
    ProductImage,
    form=ProductImageUploadForm,
    extra=1,  # Start with one empty form for uploading
    can_delete=True  # Allow deleting images
)


# Dynamic Product Option Form (Handles dynamic fields for options like Color, Size)
class DynamicProductOptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)  # Expect a Product instance
        super().__init__(*args, **kwargs)

        if product:
            # Get the product options for the product
            product_options = ProductOption.objects.filter(product=product)
            grouped_options = {}

            # Group the option values by OptionType
            for option in product_options:
                grouped_options.setdefault(option.option_type, []).extend(option.values.all())

            # Dynamically create form fields for each option type
            for option_type, option_values in grouped_options.items():
                choices = [(ov.id, ov.value) for ov in option_values]

                # Get widget class for the field type (e.g., Select, Radio, etc.)
                widget_class = self._get_widget_class(option_type)

                # Create appropriate form field based on widget type
                if widget_class == forms.CheckboxSelectMultiple:
                    self.fields[f'option_{option_type.id}'] = forms.MultipleChoiceField(
                        choices=choices,
                        label=option_type.name,
                        widget=widget_class()
                    )
                else:
                    self.fields[f'option_{option_type.id}'] = forms.ChoiceField(
                        choices=choices,
                        label=option_type.name,
                        widget=widget_class()
                    )

    def _get_widget_class(self, option_type):
        """Helper method to return appropriate widget class."""
        if option_type.field_type:
            widget_path = option_type.field_type.django_widget  # e.g., "django.forms.widgets.Select"
            try:
                module_name, class_name = widget_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                return getattr(module, class_name)
            except Exception as e:
                print(f"Error importing widget: {widget_path} - {e}")
                return forms.Select  # Fallback to Select widget
        return forms.Select  # Default widget


# Product Option Form (For creating/updating product options)
class ProductOptionForm(forms.ModelForm):
    option_type = forms.ModelChoiceField(
        queryset=ProductOptionType.objects.all(),
        widget=forms.Select,
        required=True
    )
    values = forms.ModelMultipleChoiceField(
        queryset=ProductOptionValue.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        #model = ProductOption
        fields = ['option_type', 'values']


# Product Option Value Form (For creating/updating option values like 'Red', 'Small')
class ProductOptionValueForm(forms.ModelForm):
    class Meta:
        model = ProductOptionValue
        fields = ['option_type', 'value']


# Product Variant Form (For creating/updating product variants like 'Red - Large')
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['additional_price', 'stock_quantity', 'option_values']  # Correct field names

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Product Review Form (For submitting product reviews)
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'review_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize rating field with a RadioSelect widget
        self.fields['rating'].widget = forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        
        # Use crispy forms for layout and styling
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'rating',
            'review_text',
            Submit('submit', 'Submit Review', css_class='btn btn-info')
        )

