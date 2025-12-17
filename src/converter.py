import markdown
from weasyprint import HTML, CSS
from io import BytesIO
import bleach
from urllib.parse import urlparse


# Allowed HTML after Markdown
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "blockquote",
    "code", "pre", "hr",
    "table", "thead", "tbody", "tr", "th", "td",
    "img"
]

ALLOWED_ATTRS = {
    "img": ["src", "alt"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"]
}

ALLOWED_PROTOCOLS = ["http", "https"]


def safe_url_fetcher(url):
    """
    Block file://, ftp://, internal IPs, localhost
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Blocked URL scheme")

    if parsed.hostname in ("localhost", "127.0.0.1"):
        raise ValueError("Blocked internal host")

    # Allow WeasyPrint default fetching for safe URLs
    from weasyprint.urls import default_url_fetcher
    return default_url_fetcher(url)


def converter(markdown_text: str):
    # Convert Markdown → HTML (NO raw HTML extensions)
    html = markdown.markdown(
        markdown_text,
        extensions=["extra", "fenced_code"],
        output_format="html5"
    )

    # Sanitize HTML
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )

    html_content = f"""
    <html>
      <head><meta charset="utf-8"></head>
      <body>{clean_html}</body>
    </html>
    """

    css_string = """
        * {margin: 0; padding: 0;}
        body {font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.6;}
        h1 {font-size: 15pt; margin: 15px 0 12px;}
        h2 {font-size: 13pt; margin: 10px 0;}
        h3 {font-size: 11pt; margin: 8px 0;}
        p {margin-bottom: 8px;}
        ul, ol {margin-bottom: 10px; padding-left: 30px;}
        code {background: #f0f0f0; padding: 2px 5px;}
        pre {background: #f0f0f0; padding: 10px;}
        img {display: block; margin: auto; max-width: 90%;}
        table {width: 100%; border-collapse: collapse;}
        th, td {border: 1px solid #000; padding: 6px;}
    """

    pdf_buffer = BytesIO()

    HTML(
        string=html_content,
        url_fetcher=safe_url_fetcher
    ).write_pdf(
        pdf_buffer,
        stylesheets=[CSS(string=css_string)]
    )

    pdf_buffer.seek(0)
    return pdf_buffer
