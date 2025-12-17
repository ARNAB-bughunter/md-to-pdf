from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from rate_limiter import limiter, rate_limit_exceeded_handler

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

# Attach limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

class MarkdownRequest(BaseModel):
    markdown: str
    filename: str = "document.pdf"

@app.get("/")
async def redirect_to_index():
    return FileResponse("static/index.html")

@app.post("/api/convert")
@limiter.limit("5/minute")
async def convert_md_to_pdf(request: Request, input_request: MarkdownRequest):
    try:
        if not input_request.markdown.strip():
            raise HTTPException(status_code=400, detail="Empty content")
        
        pdf_buffer = converter(input_request.markdown)
                
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={input_request.filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))