import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_SIZES = {
    "A4": A4,
    "A3": A3
}

def txt_to_pdf(input_txt, font_name="Courier", base_font_size=12, page_size=A4, landscape_mode=False):
    # Derive output name (same as input but with .pdf extension)
    root, _ = os.path.splitext(input_txt)
    output_pdf = root + ".pdf"

    font_name = "Courier"

    # Page setup
    page_size = landscape(page_size) if landscape_mode else page_size
    page_width, page_height = page_size

    # Read lines
    with open(input_txt, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find longest line
    max_line = max(lines, key=lambda l: len(l)) if lines else ""
    max_line_width = pdfmetrics.stringWidth(max_line, font_name, base_font_size)

    # Scaling factor
    margin = 40
    available_width = page_width - 2 * margin
    scale = available_width / max_line_width if max_line_width > available_width else 1.0
    font_size = base_font_size * scale

    # Create PDF
    c = canvas.Canvas(output_pdf, pagesize=page_size)
    c.setFont(font_name, font_size)

    # Write lines
    y = page_height - margin
    line_height = font_size * 1.2
    for line in lines:
        if y < margin:
            c.showPage()
            c.setFont(font_name, font_size)
            y = page_height - margin
        c.drawString(margin, y, line.rstrip())
        y -= line_height

    c.save()
    print(f"Saved: {output_pdf}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.utils.pdfprinter file1.txt [--pagesize A4] [--landscape]")
        sys.exit(1)
    
    # Defaults
    page_size = A4
    landscape_mode = False
    files = []

    # Parse args
    args = iter(sys.argv[1:])
    for arg in args:
        if arg == "--pagesize":
            size_name = next(args, "A4")
            page_size = PAGE_SIZES.get(size_name.upper(), PAGE_SIZES["A4"])
        elif arg == "--landscape":
            landscape_mode = True
        else:
            files.append(arg)

    for f in files:
        if not os.path.isfile(f):
            print(f"Skipping: {f} (not found)")
            continue
        
        txt_to_pdf(f, page_size=page_size, landscape_mode=landscape_mode)

if __name__ == "__main__":
    main()

