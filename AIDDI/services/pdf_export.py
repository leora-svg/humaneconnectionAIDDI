from io import BytesIO
from fpdf import FPDF
import markdown
import re


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Growth Plan", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)


def clean_markdown(md: str) -> list[str]:
    """
    Convert markdown into reasonably formatted plain text.
    """

    html = markdown.markdown(md)

    # Replace common HTML tags with newlines
    html = re.sub(r"<h[1-6]>", "\n\n", html)
    html = re.sub(r"</h[1-6]>", "\n", html)
    html = re.sub(r"<li>", "• ", html)
    html = re.sub(r"</li>", "\n", html)
    html = re.sub(r"<br ?/?>", "\n", html)
    html = re.sub(r"</p>", "\n\n", html)

    # Remove remaining HTML tags
    html = re.sub(r"<[^>]+>", "", html)

    return html.splitlines()


def markdown_to_pdf(markdown_text: str) -> bytes:
    pdf = PDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", size=11)

    for line in clean_markdown(markdown_text):
        line = line.strip()

        if not line:
            pdf.ln(3)
            continue

        pdf.multi_cell(0, 6, line)

    output = bytes(pdf.output())

    return output
