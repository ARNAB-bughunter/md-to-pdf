from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import markdown
from weasyprint import HTML, CSS
from io import BytesIO

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


@app.post("/api/convert")
async def convert_md_to_pdf(request: MarkdownRequest):
    try:
        if not request.markdown.strip():
            raise HTTPException(status_code=400, detail="Empty content")


        # Convert markdown to HTML
        html = markdown.markdown(
            request.markdown, 
            extensions=['extra', 'codehilite', 'fenced_code']
        )
        
        # Simple HTML structure
        html_content = f"""
            <html>
            <head></head>
            <body>{html}</body>
            </html>
        """
        
        # Your CSS styles
        css_string = """
            * {margin: 0; padding: 0;}
            body {font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.6; color: #000;}
            h1 {font-size: 15pt; font-weight: bold; margin-top: 15px; margin-bottom: 12px; color: #000; border-bottom: 1px solid #c4bdbd}
            h2 {font-size: 13pt; font-weight: bold; margin-top: 10px; margin-bottom: 10px; color: #000;}
            h3 {font-size: 11pt; font-weight: bold; margin-top: 8px; margin-bottom: 8px; color: #000;}
            p {font-size: 10pt; margin-bottom: 8px; color: #000;}
            ul, ol {margin-bottom: 10px; padding-left: 30px;}
            li {margin-bottom: 6px;}
            code {font-family: Courier New, monospace; background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-size: 11pt;}
            pre {background: #f0f0f0; padding: 10px; border-radius: 4px; font-size: 11pt; line-height: 1.5;}
            blockquote {border-left: 3px solid #ccc; padding-left: 12px; color: #555; margin: 12px 0; font-style: italic;}
            strong {font-weight: 600; color: #000;}
            hr {border-top: 2px solid #c4bdbd;}
        """
            
        # Create PDF
        pdf_buffer = BytesIO()
        HTML(string=html_content).write_pdf(
        pdf_buffer,
        stylesheets=[CSS(string=css_string)]
        )
        
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={request.filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))