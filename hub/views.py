from django.shortcuts import render


def home(request):
    tools = [
        {
            'name': 'Scanner para Excel',
            'description': 'Suba um PDF escaneado da pintura e gere uma planilha Excel com os dados extraidos.',
            'url_name': 'extrator_scanner:index',
            'status': 'Primeiro app',
            'icon': 'PDF',
        },
        {
            'name': 'Zeladoria Predial',
            'description': 'Cadastre melhorias do predio, acompanhe tickets oficiais e exporte chamados por mes.',
            'url_name': 'zeladoria:index',
            'status': 'Novo app',
            'icon': 'ZEL',
        },
    ]
    return render(request, 'hub/home.html', {'tools': tools})

# Create your views here.
