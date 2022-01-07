from django import forms

from .models import DisplayAlcoholList, StatusList


class StatusForm(forms.Form):
    status = forms.fields.ChoiceField(required=True, widget=forms.widgets.Select, choices=StatusList.CHOICES)


class DrinkForm(forms.ModelForm):
    name = forms.CharField(label='名前', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20)
    alcohol_degree = forms.IntegerField(label='アルコール度数', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'数字のみ入力'}))
    amount = forms.ChoiceField(label='サイズ', widget=forms.Select(attrs={'class': 'form-control'}), choices=DisplayAlcoholList.AMOUNT_LIST)
    memo = forms.CharField(label='メモ', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), max_length=300, required=False)
    
    class Meta:
        model = DisplayAlcoholList
        fields = ('name', 'alcohol_degree', 'amount', 'memo')