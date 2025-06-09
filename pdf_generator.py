from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.units import inch
import os
import markdown

def generate_pdf(feedback, chart_paths, output_path='student_feedback_report.pdf'):
    """
    Generate a styled PDF report using ReportLab.

    Args:
        feedback (str): Markdown-formatted feedback text.
        chart_paths (dict): Dictionary of chart names to their file paths.
        output_path (str): Path to save the generated PDF.

    Returns:
        str: Path to the generated PDF.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add a title
    title = Paragraph("Student Performance Feedback Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5 * inch))

    # Convert Markdown feedback to plain text
    feedback_html = markdown.markdown(feedback)  # Convert Markdown to HTML
    # Strip HTML tags to get plain text, preserving line breaks
    feedback_text = ''.join(feedback_html.replace('<p>', '').replace('</p>', '\n')
                            .replace('<strong>', '').replace('</strong>', '')
                            .replace('<em>', '').replace('</em>', '')
                            .replace('<br>', '\n'))
    feedback_paragraphs = feedback_text.split('\n')

    # Add each paragraph to the PDF
    for para in feedback_paragraphs:
        if para.strip():  # Skip empty lines
            p = Paragraph(para, styles['BodyText'])
            story.append(p)
            story.append(Spacer(1, 0.2 * inch))

    # Add chart images
    for chart_name, chart_path in chart_paths.items():
        img = Image(chart_path, width=6*inch, height=4*inch)
        story.append(Paragraph(chart_name, styles['Heading2']))
        story.append(img)
        story.append(Spacer(1, 0.5 * inch))

    # Build the PDF
    doc.build(story)

    # Clean up temporary chart images
    for path in chart_paths.values():
        if os.path.exists(path):
            os.remove(path)

    return output_path