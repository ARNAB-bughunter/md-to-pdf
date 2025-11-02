from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML, CSS
from io import BytesIO

from src.converter import converter

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class MarkdownRequest(BaseModel):
    markdown: str
    filename: str = "document.pdf"




@app.get("/")
async def redirect_to_index():
    return FileResponse("static/index.html")

@app.get("/login")
async def login():
    return FileResponse("static/login.html")

@app.post("/api/convert")
async def convert_md_to_pdf(request: MarkdownRequest):
    try:
        if not request.markdown.strip():
            raise HTTPException(status_code=400, detail="Empty content")
        
        pdf_buffer = converter(request.markdown)
                
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={request.filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))