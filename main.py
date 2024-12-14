from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from markitdown import MarkItDown
import os
from typing import Optional
import tempfile
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("A variável SECRET_KEY não foi encontrada no .env!")

@app.middleware("http")
async def verify_token(request, call_next):
    if request.url.path == "/upload":
        token = request.headers.get("Authorization")
        if not token or token != SECRET_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "Não autorizado"}
            )
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "API de conversão de documentos para Markdown", "version": "1.0.0", "author": "Antonio Abrantes", "github": "https://github.com/antonio-abrantes"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = [
        'pdf', 'pptx', 'docx', 'doc', 'xlsx', 
        'txt', 'csv', 'json', 'xml', 'html'
    ]
    
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        markitdown = MarkItDown()
        result = markitdown.convert(temp_path)
        
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = f"{timestamp}.md"
        
        os.unlink(temp_path)
        
        markdown_content = result.text_content.replace('\r\n', '\n').strip()
        
        return {
            "filename": filename,
            "markdown": markdown_content,
            "success": True
        }
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
