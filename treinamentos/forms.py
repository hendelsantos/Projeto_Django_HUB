from django import forms

from .models import TreinamentoSeguranca


class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = TreinamentoSeguranca
        fields = [
            'titulo',
            'categoria',
            'status',
            'data',
            'hora_inicio',
            'hora_fim',
            'empresa',
            'area',
            'instrutor',
            'carga_horaria',
            'validade',
            'documento',
            'texto_participantes',
            'observacoes',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex.: Treinamento de seguranca na pintura'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'empresa': forms.TextInput(attrs={'placeholder': 'Ex.: Paint Shop, Terceiro, Fornecedor'}),
            'area': forms.TextInput(attrs={'placeholder': 'Ex.: Pintura, Preparacao, Cabine'}),
            'instrutor': forms.TextInput(attrs={'placeholder': 'Nome do instrutor'}),
            'carga_horaria': forms.TextInput(attrs={'placeholder': 'Ex.: 2h, 4h, 8h'}),
            'validade': forms.DateInput(attrs={'type': 'date'}),
            'texto_participantes': forms.Textarea(
                attrs={
                    'rows': 8,
                    'placeholder': 'Opcional. Em PDF digital o sistema tenta ler sozinho. Para scanner/imagem, cole os nomes aqui. Formato: Nome; matricula; turno; area; empresa',
                }
            ),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Observacoes, conteudo aplicado ou pontos importantes'}),
        }
