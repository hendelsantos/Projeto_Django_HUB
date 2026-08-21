# Paint Hub

Projeto Django para reunir ferramentas internas simples do departamento de pintura em um painel central.

## Decisoes iniciais

- Banco de dados: SQLite, simples para desenvolvimento e uso local.
- Interface: HTML com CSS proprio, bonita mas facil de manter.
- Estrutura: cada ferramenta deve virar um app Django separado.
- Primeiro app: extrator de scanner/PDF para gerar planilha Excel.

## Como rodar

```bash
source .venv/bin/activate
python manage.py runserver 127.0.0.1:8010
```

Depois acesse:

```text
http://127.0.0.1:8010/
```

## Estrutura atual

- `hub`: pagina central com os botoes das ferramentas.
- `extrator_scanner`: upload de PDF e geracao inicial de Excel.
- `zeladoria`: cadastro e acompanhamento de necessidades de zeladoria predial.
- `templates`: paginas HTML compartilhadas e dos apps.
- `static/css/styles.css`: estilo visual simples do projeto.

## Proximos passos do extrator

Quando a estrutura do Excel escaneado estiver definida, o extrator deve ser ajustado para:

- Ler os campos certos do PDF.
- Montar as colunas finais do Excel.
- Validar se algum dado esperado nao foi encontrado.
- Opcionalmente guardar historico dos arquivos processados no SQLite.
