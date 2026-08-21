from django import forms

from .models import Armario


class ArmarioForm(forms.ModelForm):
    class Meta:
        model = Armario
        fields = [
            'numero',
            'usuario',
            'turno',
            'tamanho_camisa',
            'tamanho_calca',
            'tamanho_macacao',
            'status',
            'observacoes',
        ]
        widgets = {
            'numero': forms.NumberInput(attrs={'placeholder': 'Ex.: 1, 2, 3'}),
            'usuario': forms.TextInput(attrs={'placeholder': 'Nome de quem usa o armario'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Informacoes adicionais, troca, pendencia ou manutencao'}),
        }
