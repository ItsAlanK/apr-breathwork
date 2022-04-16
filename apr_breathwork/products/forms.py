from django import forms
from .models import Product, ProductVariant, Category


class ProductForm(forms.ModelForm):
    """ Form for managing products from front end. """

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-grey rounded'


class ProductVariantForm(forms.ModelForm):
    """ Form for managing product variants from front end. """

    class Meta:
        """ Set fields for variant form """
        model = ProductVariant
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            'time': forms.TimeInput(
                format=('%H:%M'),
                attrs={'class': 'form-control',
                    'placeholder': 'Select a time',
                    'type': 'time'
                    }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-grey rounded'
