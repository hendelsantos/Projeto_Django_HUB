from django import forms

from .models import Tarefa


class TarefaCreateForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'responsavel', 'area', 'origem', 'prioridade', 'prazo']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex.: Cobrar retorno do chamado, validar lista, conferir armario'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explique o que precisa ser acompanhado'}),
            'responsavel': forms.TextInput(attrs={'placeholder': 'Nome do responsavel'}),
            'area': forms.TextInput(attrs={'placeholder': 'Ex.: Pintura, TI, Roupeiro, Zeladoria'}),
            'origem': forms.TextInput(attrs={'placeholder': 'App, processo ou reuniao de origem'}),
            'prazo': forms.DateInput(attrs={'type': 'date'}),
        }


class TarefaFollowUpForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['status', 'prioridade', 'responsavel', 'area', 'origem', 'prazo', 'follow_up']
        widgets = {
            'responsavel': forms.TextInput(attrs={'placeholder': 'Nome do responsavel'}),
            'area': forms.TextInput(attrs={'placeholder': 'Area relacionada'}),
            'origem': forms.TextInput(attrs={'placeholder': 'App, processo ou reuniao de origem'}),
            'prazo': forms.DateInput(attrs={'type': 'date'}),
            'follow_up': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Registre a baixa, retorno, pendencia ou proximo passo'}),
        }
