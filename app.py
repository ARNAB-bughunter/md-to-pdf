from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from rate_limiter import limiter, rate_limit_exceeded_handler
from starlette.middleware.base import BaseHTTPMiddleware
from src.converter import converter
from mangum import Mangum
# from utils.minify import minify_static_files
import os

os.environ["FONTCONFIG_PATH"] = "/etc/fonts"
os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["HOME"] = "/tmp"
os.environ["TMPDIR"] = "/tmp"




# minify_static_files()

app = FastAPI(docs_url=None,redoc_url=None)
MAX_REQUEST_SIZE = 2 * 1024 * 1024  # 2MB
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)

class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > MAX_REQUEST_SIZE:
                return JSONResponse(
                    status_code=413,
                    content={
                        "status_code": 413,
                        "message": "Request too large"
                    }
                )
        return await call_next(request)

app.add_middleware(RequestSizeLimitMiddleware)

# Attach limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

class MarkdownRequest(BaseModel):
    markdown: str
    filename: str = "document.pdf"
    @field_validator('filename')
    def sanitize_filename(cls, v):
        # Remove path traversal attempts
        import os
        v = os.path.basename(v)
        # Remove dangerous characters
        v = "".join(c for c in v if c.isalnum() or c in (' ', '.', '_', '-'))
        if not v.endswith('.pdf'):
            v += '.pdf'
        return v


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    # JSON (API use case)
    return FileResponse("static/404_page.html")

@app.get("/")
async def redirect_to_index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/convert")
@limiter.limit("5/minute")
async def convert_md_to_pdf(request: Request, input_request: MarkdownRequest):
    try:
        if not input_request.markdown.strip():
            raise HTTPException(status_code=400, detail="Empty content")
        
        pdf_buffer = converter(input_request.markdown)
                
        return Response(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={input_request.filename}"}
        )
        
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")