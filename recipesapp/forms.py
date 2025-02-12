from django import forms
from recipesapp.models import Category, Recipe


class RecipeForm(forms.ModelForm):
    """
    Форма ввода рецепта
    """
    class Meta:
        model = Recipe
        exclude = ['post_date']
        fields = ['title',
                  'description',
                  'ingredients',
                  'cooking_steps',
                  'cooking_time',
                  'photo',
                  'category'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'cooking_steps': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].widget = forms.Select(attrs={'class': 'form-control'})



class CategoryForm(forms.ModelForm):
    """
    Форма добавления категории (в разработке)
    """
    class Meta:
        model = Category
        fields = ['name']

