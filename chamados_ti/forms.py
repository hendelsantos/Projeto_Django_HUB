from django import forms

from .models import ChamadoTI


class ChamadoTICreateForm(forms.ModelForm):
    class Meta:
        model = ChamadoTI
        fields = ['titulo', 'solicitante', 'setor', 'categoria', 'prioridade', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex.: Criar conta, verificar notebook, acesso ao sistema'}),
            'solicitante': forms.TextInput(attrs={'placeholder': 'Nome de quem esta solicitando'}),
            'setor': forms.TextInput(attrs={'placeholder': 'Ex.: Pintura, Qualidade, Manutencao'}),
            'descricao': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descreva o problema ou necessidade'}),
        }


class ChamadoTIFollowUpForm(forms.ModelForm):
    class Meta:
        model = ChamadoTI
        fields = ['status', 'ticket_oficial', 'solucao']
        widgets = {
            'ticket_oficial': forms.TextInput(attrs={'placeholder': 'Numero do chamado no sistema oficial, se houver'}),
            'solucao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Atendimento realizado, retorno, pendencia ou solucao'}),
        }
