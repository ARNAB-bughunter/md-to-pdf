import markdown
from weasyprint import HTML, CSS

def md_to_pdf(markdown_file, pdf_file):
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html = markdown.markdown(
            md_content, 
            extensions=['extra', 'codehilite', 'fenced_code']
        )
        
    

    HTML(string=html).write_pdf(pdf_file, counter_style=[CSS(string='body {{font-family: Helvetica, Arial, sans-serif;font-size: 12pt;line-height: 1.6;color: #000;margin: 5px;}}')])


# Usage
md_to_pdf('input.md', 'output.pdf')