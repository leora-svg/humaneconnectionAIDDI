from fpdf import FPDF
import markdown
import re
import os


FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # Unicode fonts
        self.add_font(
            "DejaVu",
            "",
            FONT_PATH
        )
        self.add_font(
            "DejaVu",
            "B",
            FONT_BOLD_PATH
        )

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(
            0,
            10,
            "Growth Plan",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )
        self.ln(5)


def clean_markdown(md: str) -> list[str]:
    """
    Convert markdown into reasonably formatted plain text.
    """

    html = markdown.markdown(md)

    html = re.sub(r"<h[1-6]>", "\n\n", html)
    html = re.sub(r"</h[1-6]>", "\n", html)
    html = re.sub(r"<li>", "• ", html)
    html = re.sub(r"</li>", "\n", html)
    html = re.sub(r"<br ?/?>", "\n", html)
    html = re.sub(r"</p>", "\n\n", html)

    html = re.sub(r"<[^>]+>", "", html)

    return html.splitlines()


def markdown_to_pdf(markdown_text: str) -> bytes:
    pdf = PDF()

    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVu", size=11)

    for line in clean_markdown(markdown_text):
        line = line.strip()

        if not line:
            pdf.ln(3)
            continue

        pdf.multi_cell(0, 6, line)

    output = bytes(pdf.output())

    return output
