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
            'tamanho_camisa_numero',
            'tamanho_calca',
            'tamanho_calca_numero',
            'tamanho_macacao',
            'tamanho_macacao_numero',
            'status',
            'observacoes',
        ]
        widgets = {
            'numero': forms.NumberInput(attrs={'placeholder': 'Ex.: 1, 2, 3'}),
            'usuario': forms.TextInput(attrs={'placeholder': 'Nome de quem usa o armario'}),
            'tamanho_camisa_numero': forms.NumberInput(attrs={'placeholder': 'Ex.: 38, 40, 42'}),
            'tamanho_calca_numero': forms.NumberInput(attrs={'placeholder': 'Ex.: 38, 40, 42'}),
            'tamanho_macacao_numero': forms.NumberInput(attrs={'placeholder': 'Ex.: 38, 40, 42'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Informacoes adicionais, troca, pendencia ou manutencao'}),
        }
