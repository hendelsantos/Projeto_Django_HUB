# Paint Hub

Projeto Django para reunir ferramentas internas simples do departamento de pintura em um painel central.

## Decisoes iniciais

- Banco de dados: SQLite, simples para desenvolvimento e uso local.
- Interface: HTML com CSS proprio, bonita mas facil de manter.
- Estrutura: cada ferramenta deve virar um app Django separado.
- Primeiro app: extrator de scanner/PDF para gerar planilha Excel.

## Como rodar

### Linux

```bash
chmod +x scripts/start_linux.sh
./scripts/start_linux.sh
```

### Windows

```bat
scripts\start_windows.bat
```

Depois acesse nesta maquina:

```text
http://127.0.0.1:8010/
```

Para acessar pela rede, use o IP da maquina que esta rodando o sistema:

```text
http://IP-DA-MAQUINA:8010/
```

Exemplo:

```text
http://192.168.0.25:8010/
```

Se quiser trocar a porta:

Linux:

```bash
PAINT_HUB_PORT=8020 ./scripts/start_linux.sh
```

Windows:

```bat
set PAINT_HUB_PORT=8020
scripts\start_windows.bat
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
