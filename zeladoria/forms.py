from django import forms

from .models import ChamadoZeladoria


class ChamadoCreateForm(forms.ModelForm):
    class Meta:
        model = ChamadoZeladoria
        fields = ['solicitante', 'local', 'descricao', 'foto']
        widgets = {
            'solicitante': forms.TextInput(attrs={'placeholder': 'Nome de quem esta solicitando'}),
            'local': forms.TextInput(attrs={'placeholder': 'Ex.: Predio 2, corredor, sala, banheiro'}),
            'descricao': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descreva o que precisa ser melhorado'}),
        }


class ChamadoFollowUpForm(forms.ModelForm):
    class Meta:
        model = ChamadoZeladoria
        fields = ['status', 'ticket_oficial', 'observacoes']
        widgets = {
            'ticket_oficial': forms.TextInput(attrs={'placeholder': 'Numero do ticket no sistema oficial'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ultimo acompanhamento, prazo ou retorno recebido'}),
        }
