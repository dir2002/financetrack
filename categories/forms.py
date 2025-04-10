from django import forms
from .models import Category, SubCategory

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'subcategory']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            category = self.data.get('category')
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=category)
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.none())