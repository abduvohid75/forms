from django import forms
from main.models import blog, Product, Category, Version

class StyleForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'status': # form-control не подружился с полем статуса, пришлось прописывать условие
                field.widget.attrs['class'] = 'form-control'
class BlogForm(StyleForm, forms.ModelForm):

    class Meta:
        model = blog
        fields = ('name', 'description', 'preview',)

class ProductForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Недопустимые слова в названии продукта")
        return cleaned_data

class VersionForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Version
        fields = "__all__"