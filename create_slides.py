from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def parse_analysis_file(file_path):
    """Parse the analysis file and extract slide contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into slides
    slides = re.split(r'={50,}\nSLIDE \d+\n={50,}\n\n', content)
    # Remove empty slides
    slides = [slide.strip() for slide in slides if slide.strip()]
    return slides

def create_pdf_from_slides(slides, output_path):
    """Create a PDF presentation from slide contents."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Define styles
    title_style = ParagraphStyle(
        'TitleStyle',
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        fontSize=16,
        leading=24,
        alignment=TA_LEFT,
    )
    
    for slide_content in slides:
        # Remove quotes if present
        slide_content = slide_content.strip('"')
        
        # Create slide
        p = Paragraph(slide_content, body_style)
        
        # Get required height
        w, h = p.wrap(width - 72, height - 72)  # 72 points = 1 inch margin
        
        # Draw the text
        p.drawOn(c, 36, height - h - 36)  # 36 points = 0.5 inch margin
        
        c.showPage()
    
    c.save()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convert analysis text to PDF slides')
    parser.add_argument('input_file', help='Path to the analysis text file')
    parser.add_argument('--output', default='output_slides.pdf', help='Output PDF path')
    
    args = parser.parse_args()
    
    # Parse slides from analysis file
    slides = parse_analysis_file(args.input_file)
    
    # Create PDF
    create_pdf_from_slides(slides, args.output)
    print(f"Created PDF presentation at: {args.output}")

if __name__ == "__main__":
    main() 