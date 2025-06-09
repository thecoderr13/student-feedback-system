from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os
import markdown

def generate_pdf(feedback, chart_paths, output_path='student_feedback_report.pdf'):
    """
    Generate a styled PDF report using ReportLab with reduced spacing, page numbering, and charts on new pages.
    Text sections are condensed to fit on single pages where specified.

    Args:
        feedback (str): Markdown-formatted feedback text.
        chart_paths (dict): Dictionary of chart names to their file paths.
        output_path (str): Path to save the generated PDF.

    Returns:
        str: Path to the generated PDF.
    """
    # Initialize the document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Define custom styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CenteredTitle',
        parent=styles['Title'],
        alignment=1,  # Center alignment
        fontSize=16,  # Reduced font size
        spaceAfter=0.3*inch  # Reduced spacing
    ))
    styles.add(ParagraphStyle(
        name='BodyTextIndented',
        parent=styles['BodyText'],
        leftIndent=0.25*inch,
        fontSize=10,  # Reduced font size for compact text
        spaceAfter=0.1*inch,  # Tighter spacing
        spaceBefore=0.05*inch  # Minimal space before
    ))
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,  # Smaller heading size
        spaceAfter=0.15*inch,  # Reduced spacing
        spaceBefore=0.2*inch
    ))

    story = []

    # Add a title
    title = Paragraph("Student Performance Feedback Report", styles['CenteredTitle'])
    story.append(title)
    story.append(Spacer(1, 0.3 * inch))  # Reduced spacer

    # Convert Markdown feedback to plain text
    feedback_html = markdown.markdown(feedback)  # Convert Markdown to HTML
    feedback_text = ''.join(feedback_html.replace('<p>', '').replace('</p>', '\n')
                           .replace('<strong>', '').replace('</strong>', '')
                           .replace('<em>', '').replace('</em>', '')
                           .replace('<br>', '\n'))
    
    # Split feedback into sections based on headings (assumes Markdown headings like ##)
    sections = feedback_text.split('\n## ')
    section_titles = ['Introduction and Performance Breakdown', 
                     'Subject-wise, Chapter-wise, Difficulty-wise, and Concept-wise Performance', 
                     'Time vs. Accuracy Insights and Actionable Suggestions']

    # Process each section
    for i, section in enumerate(sections):
        if section.strip():
            # Extract section title and content
            section_lines = section.strip().split('\n', 1)
            section_title = section_lines[0].replace('## ', '').strip()
            section_content = section_lines[1].strip() if len(section_lines) > 1 else ''
            
            # Check if section matches one of the specified sections
            if section_title in section_titles:
                # Add section heading
                heading = Paragraph(section_title, styles['SectionHeading'])
                story.append(heading)
                
                # Split content into paragraphs
                paragraphs = section_content.split('\n')
                for para in paragraphs:
                    if para.strip():  # Skip empty lines
                        p = Paragraph(para, styles['BodyTextIndented'])
                        story.append(p)
                        story.append(Spacer(1, 0.05 * inch))  # Tighter spacer
                
                # Add page break after each specified section to ensure single-page layout
                story.append(PageBreak())
            else:
                # Handle other sections with minimal spacing
                heading = Paragraph(section_title, styles['SectionHeading'])
                story.append(heading)
                paragraphs = section_content.split('\n')
                for para in paragraphs:
                    if para.strip():
                        p = Paragraph(para, styles['BodyTextIndented'])
                        story.append(p)
                        story.append(Spacer(1, 0.05 * inch))

    # Add chart images, each on a new page (unchanged)
    for chart_name, chart_path in chart_paths.items():
        story.append(PageBreak())  # Start chart on new page
        chart_title = Paragraph(chart_name, styles['Heading2'])
        story.append(chart_title)
        story.append(Spacer(1, 0.3 * inch))
        img = Image(chart_path, width=6*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 0.5 * inch))

    # Define page numbering
    def add_page_numbers(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont("Helvetica", 9)
        canvas.drawRightString(doc.width + doc.leftMargin, 0.5 * inch, text)

    # Build the PDF with page numbering
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)

    # Clean up temporary chart images
    for path in chart_paths.values():
        if os.path.exists(path):
            os.remove(path)

    return output_path