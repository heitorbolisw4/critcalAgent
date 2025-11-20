# Critical Agent - Scanner de Seguranca AppSec

Ferramenta em Python que analisa codigo PHP e paginas estaticas (HTML, CSS, JS) para achados de SQL Injection, XSS e problemas de validacao de entrada. Usa o modelo `llama-3.3-70b-versatile` via Groq e sempre responde em portugues.

## 🤝 O que voce precisa
- Python 3.10+
- Chave da API Groq (`GROQ_API_KEY`)

## ⚙️ Configuracao rapida
1) Clone o repositorio.
2) Crie um `.env` na raiz:
```
GROQ_API_KEY=seu_token_aqui
# Opcional: base de projetos
PROJECTS_ROOT=/caminho/para/projetos
```
3) Instale dependencias:
```
pip install -r requirements.txt
```
Se nao tiver `requirements.txt`, instale manualmente:
```
pip install langchain-groq langchain-core python-dotenv
```

## 🚀 Como usar
- **Scan de projeto** (gera `security_report.md`):
```
python critcalAgent.py --scan /caminho/do/projeto
```
Se `PROJECTS_ROOT` estiver setado, voce pode passar so o nome do projeto.

- **Modo interativo** (colar trechos ou perguntas):
```
python critcalAgent.py --interactive
```
Digite `x` para sair.

## 🔍 O que o agente faz
- Varre recursivamente `.php`, `.html`, `.htm`, `.js`, `.css`.
- Envia o conteudo para o LLM com prompt especializado em AppSec (PHP + paginas estaticas).
- Retorna: tipo da vulnerabilidade, linha aproximada, gravidade e sugestao de correcao.

## 🖼️ Visualizando o fluxo
1) 📨 Voce fornece o caminho do projeto ou trecho de codigo.
2) 🤖 O agente envia cada arquivo elegivel para analise pelo modelo.
3) 🛡️ Recebe um relatorio em portugues com achados e correcoes sugeridas.

## 🛡️ Boas praticas
- `security_report.md` e `.vs/` estao no `.gitignore` para evitar vazamentos; ajuste se quiser versiona-los.
- Nunca versione sua `GROQ_API_KEY`. Regere a chave se ja esteve exposta.
- Quer suportar novas extensoes (ex.: `.vue`, `.jsx`)? Edite `scan_directory` em `critcalAgent.py`.

## 🧪 Dicas de teste rapido
- Rode o scan em uma pasta pequena com um `.php` de exemplo para validar a saida.
- No modo interativo, cole um snippet curto para ver a resposta formatada.
