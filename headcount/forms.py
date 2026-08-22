from django import forms


class HeadcountUploadForm(forms.Form):
    mes = forms.DateField(
        label='Mes de referencia',
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m', '%Y-%m-%d'],
    )
    headcount_file = forms.FileField(label='Arquivo Excel do headcount')
    birthday_image = forms.ImageField(label='Foto/lista de aniversariantes do mes')
    birthday_text = forms.CharField(
        label='Texto da foto de aniversariantes',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 6,
                'placeholder': 'Cole aqui os nomes lidos da foto, um por linha. O OCR podera ser conectado depois.',
            }
        ),
    )
