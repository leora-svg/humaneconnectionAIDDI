import markdown
from io import BytesIO
from xhtml2pdf import pisa

def markdown_to_pdf(markdown_text):
    html = markdown.markdown(markdown_text)

    output = BytesIO()
    pisa.CreatePDF(html, dest=output)

    return output.getvalue()
