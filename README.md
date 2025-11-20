# Critical Agent - Scanner de Segurança AppSec

Ferramenta em Python para analisar código PHP e páginas estáticas (HTML, CSS, JS), buscando principalmente SQL Injection, XSS e problemas de validação de entrada. Usa o modelo `llama-3.3-70b-versatile` via Groq para gerar relatórios em português.

## Requisitos
- Python 3.10+
- Conta e chave da API Groq (`GROQ_API_KEY`)

## Configuração
1) Clone o repositório.
2) Crie um arquivo `.env` na raiz com:
```
GROQ_API_KEY=seu_token_aqui
# Opcional: caminho base para projetos
PROJECTS_ROOT=/caminho/para/projetos
```
3) Instale dependências:
```
pip install -r requirements.txt
```
(se ainda não houver `requirements.txt`, instale manualmente: `pip install langchain-groq langchain-core python-dotenv`).

## Uso
### Scan de projeto
gera `security_report.md` na raiz:
```
python critcalAgent.py --scan /caminho/do/projeto
```
Você também pode passar apenas o nome do projeto se `PROJECTS_ROOT` estiver setado.

### Modo interativo
Para colar trechos de código ou perguntas diretamente:
```
python critcalAgent.py --interactive
```
Digite `x` para sair.

## Como funciona
- Varre recursivamente por arquivos `.php`, `.html`, `.htm`, `.js`, `.css`.
- Envia o conteúdo para o LLM com um prompt especializado em AppSec (PHP + páginas estáticas).
- Retorna um relatório conciso em português com tipo de vulnerabilidade, linha aproximada, gravidade e sugestão de correção.

## Notas
- O arquivo `security_report.md` é gerado e já está ignorado no `.gitignore` para evitar commits acidentais; ajuste se quiser versioná-lo.
- Mantenha sua chave da API em `.env` e não a versione.
- Para adicionar novas extensões (ex.: `.vue`, `.jsx`), edite `scan_directory` em `critcalAgent.py`.
# critcalAgent
# critcalAgent
