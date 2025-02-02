import os
from pathlib import Path
import pdf2image
import time
from llm import ImageAnalyzer
import argparse
import tempfile
import platform
import subprocess

def get_poppler_path():
    """Get the path to poppler binaries based on the operating system."""
    if platform.system() == "Darwin":  # macOS
        try:
            # Try to get poppler path from homebrew
            brew_path = subprocess.run(
                ["brew", "--prefix", "poppler"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            return f"{brew_path}/bin"
        except (subprocess.SubprocessError, FileNotFoundError):
            return None
    return None

def process_pdf_slides(pdf_path: str, context: str = None, output_dir: str = "output", start_slide: int = 1):
    """
    Process PDF slides, convert to images, and analyze them using the ImageAnalyzer.
    
    Args:
        pdf_path: Path to the PDF file
        context: Optional context for image analysis
        output_dir: Directory to save the output text file
        start_slide: Slide number to start processing from (for resume capability)
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Create a subdirectory for slides
    pdf_name = Path(pdf_path).stem
    slides_dir = output_dir / f"{pdf_name}_slides"
    slides_dir.mkdir(exist_ok=True)
    
    # Initialize image analyzer
    analyzer = ImageAnalyzer()
    output_file = output_dir / f"{pdf_name}_analysis.txt"
    
    # Get poppler path for macOS
    poppler_path = get_poppler_path()
    
    # Convert PDF to images
    print(f"Converting PDF: {pdf_path}")
    slides = pdf2image.convert_from_path(
        pdf_path,
        dpi=150,  # Reduced from 300 for smaller file sizes while maintaining readability
        fmt='jpeg',
        thread_count=os.cpu_count(),
        poppler_path=poppler_path
    )
    
    print(f"Total slides found: {len(slides)}")
    
    # Process each slide
    for i, slide in enumerate(slides, start=1):
        if i < start_slide:
            continue
            
        try:
            print(f"Processing slide {i}/{len(slides)}")
            
            # Save slide as image in the permanent slides directory
            slide_path = slides_dir / f"slide_{i:03d}.jpg"
            slide.save(slide_path, "JPEG", quality=95)
            
            # Analyze the image
            analysis = analyzer.analyze_image(
                str(slide_path),
                context=context
            )
            
            # Write analysis to file
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\nSLIDE {i}\n{'='*50}\n\n")
                f.write(analysis)
                f.write("\n\n")
            
            # Sleep to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing slide {i}: {str(e)}")
            print(f"You can resume from slide {i} using --start-slide {i}")
            raise
            
    print(f"Analysis complete. Output saved to: {output_file}")
    print(f"Slide images saved in: {slides_dir}")

def main():
    parser = argparse.ArgumentParser(description='Process PDF slides and analyze them')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--context', help='Optional context for image analysis')
    parser.add_argument('--output-dir', default='output', help='Output directory for analysis')
    parser.add_argument('--start-slide', type=int, default=1, help='Slide number to start from')
    
    args = parser.parse_args()
    
    process_pdf_slides(
        args.pdf_path,
        context=args.context,
        output_dir=args.output_dir,
        start_slide=args.start_slide
    )

if __name__ == "__main__":
    main()
