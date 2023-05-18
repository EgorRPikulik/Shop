import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, MultipleChoiceField

from .models import Card, Product, Category

    

class CardCreationForm(ModelForm):
    """ Form for creation Card instance"""

    class Meta:
        model = Card
        exclude = ['user']
        
    
    def clean(self):
        super(CardCreationForm, self).clean()
        
        card_number = self.cleaned_data.get('number')
        
        validity_period = self.cleaned_data.get('validity_period')
        date = datetime.datetime.strptime(validity_period, "%m/%y").date()
        
        if datetime.date.today() > date or len(validity_period) != 5:
            self._errors['validity_period'] = self.error_class(['Invalid validity period'])
            
        if len(card_number) != 16:
            self._errors['number'] = self.error_class(['Invalid card number'])
            
        return self.cleaned_data



    def __init__(self, *args, **kwargs):
        super(CardCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class CategoryCreationForm(Form):
   # CHOISES = tuple((num, category) for num, category in enumerate(Category.objects.all()))

    #categories = MultipleChoiceField(choices=CHOISES)

    
    def __init__(self, *args, **kwargs) -> None:
       # self.categories = tuple((num, category) for num, category in enumerate(Category.objects.all()))
        super().__init__(*args, **kwargs)


class ProductCreationForm(ModelForm):
    """ Form for creation Publication instance"""

    class Meta:
        model = Product
        exclude = ['image_url', 'category']

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
