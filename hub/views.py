from django.shortcuts import render


def home(request):
    tools = [
        {
            'name': 'Scanner para Excel',
            'description': 'Suba um PDF escaneado da pintura e gere uma planilha Excel com os dados extraidos.',
            'details': 'Use quando receber arquivos de scanner e precisar transformar o conteudo em uma planilha para conferencia ou tratamento.',
            'url_name': 'extrator_scanner:index',
            'status': 'Primeiro app',
            'icon': 'PDF',
        },
        {
            'name': 'Zeladoria Predial',
            'description': 'Cadastre melhorias do predio, acompanhe tickets oficiais e exporte chamados por mes.',
            'details': 'Ideal para registrar pedidos da equipe sobre estrutura predial, inserir foto, fazer follow-up e controlar o que ainda esta aberto.',
            'url_name': 'zeladoria:index',
            'status': 'Novo app',
            'icon': 'ZEL',
        },
        {
            'name': 'Chamados de TI',
            'description': 'Controle atendimentos de TI, contas, sistemas e equipamentos com metricas mensais.',
            'details': 'Organiza demandas como abertura de conta, acesso a sistemas, verificacao de equipamentos e relatorio de atendimentos do mes.',
            'url_name': 'chamados_ti:index',
            'status': 'Gestao',
            'icon': 'TI',
        },
    ]
    return render(request, 'hub/home.html', {'tools': tools})

# Create your views here.
