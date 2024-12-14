# API de Conversão de Documentos para Markdown

Esta API permite converter diversos tipos de documentos para formato Markdown usando a biblioteca (MarkItDown)[https://github.com/microsoft/markitdown] da Microsoft.

## Funcionalidades

- Endpoint `/upload` para envio de arquivos
- Suporte para diversos formatos: PDF, PPTX, DOCX, DOC, XLSX, TXT, CSV, JSON, XML, HTML
- Autenticação via header com chave secreta
- Retorno em formato Markdown

## Requisitos

- Python 3.9+
- Docker e Docker Compose (para deploy)

## Instalação Local

1. Clone o repositório
2. Crie um ambiente virtual: 
```
python -m venv venv
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```
3. Instale as dependências:
```
pip install -r requirements.txt
```
4. Crie o arquivo .env com a chave secreta:
```
SECRET_KEY=sua_chave_secreta
```
5. Rode a API:
```
python main.py
```
ou
```
uvicorn main:app --reload
```

## Deploy com Docker

1. Certifique-se de ter Docker e Docker Compose instalados
2. Crie a rede Docker:
```
docker network create sua_rede
```
3. Execute:
```
docker-compose up -d
```


## Uso da API

Para converter um arquivo, faça uma requisição POST para `/upload`:
```
curl -X POST "http://localhost:8000/upload" \
-H "Authorization: sua_chave_secreta" \
-F "file=@seu_arquivo.pdf"
```

### Resposta

```json
{
    "filename": "2024-03-14-153022.md",
    "markdown": "Conteúdo convertido em markdown",
    "success": true
}
```

## Notas de Segurança

- Sempre mantenha a SECRET_KEY segura
- Em produção, use variáveis de ambiente para configurações sensíveis
- Recomenda-se usar HTTPS em produção

criado com ❤️ por [Antonio Abrantes](https://github.com/antonio-abrantes)
