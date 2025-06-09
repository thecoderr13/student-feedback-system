from flask import Flask, request, send_file, render_template, redirect, url_for, session
import os
from data_processing import process_data
from llm_feedback import generate_feedback
from chart_generator import generate_charts
from pdf_generator import generate_pdf
import json
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-to-something-secure'  # Change this to a secure secret key

# Ensure uploads and reports directories exist
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
for folder in [UPLOAD_FOLDER, REPORTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def serialize_processed_data(processed_data):
    """Convert tuple keys to strings for session storage"""
    serialized = processed_data.copy()
    
    # Convert chapter_metrics tuple keys to strings
    if 'chapter_metrics' in serialized:
        chapter_metrics_str = {}
        for (subject, chapter), metrics in serialized['chapter_metrics'].items():
            key = f"{subject}|{chapter}"
            chapter_metrics_str[key] = metrics
        serialized['chapter_metrics'] = chapter_metrics_str
    
    # Convert concept_metrics tuple keys to strings
    if 'concept_metrics' in serialized:
        concept_metrics_str = {}
        for (subject, concept), metrics in serialized['concept_metrics'].items():
            key = f"{subject}|{concept}"
            concept_metrics_str[key] = metrics
        serialized['concept_metrics'] = concept_metrics_str
    
    return serialized

def deserialize_processed_data(serialized_data):
    """Convert string keys back to tuples"""
    processed_data = serialized_data.copy()
    
    # Convert chapter_metrics string keys back to tuples
    if 'chapter_metrics' in processed_data:
        chapter_metrics_tuples = {}
        for key, metrics in processed_data['chapter_metrics'].items():
            subject, chapter = key.split('|', 1)
            chapter_metrics_tuples[(subject, chapter)] = metrics
        processed_data['chapter_metrics'] = chapter_metrics_tuples
    
    # Convert concept_metrics string keys back to tuples
    if 'concept_metrics' in processed_data:
        concept_metrics_tuples = {}
        for key, metrics in processed_data['concept_metrics'].items():
            subject, concept = key.split('|', 1)
            concept_metrics_tuples[(subject, concept)] = metrics
        processed_data['concept_metrics'] = concept_metrics_tuples
    
    return processed_data

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            # Generate unique session ID for this report
            report_id = str(uuid.uuid4())
            session['current_report_id'] = report_id
            
            filepath = os.path.join(UPLOAD_FOLDER, f"{report_id}_{file.filename}")
            file.save(filepath)
            
            try:
                # Process the uploaded JSON file
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle both list and dict formats
                    if isinstance(data, list):
                        data = data[0]  # Take first element if it's a list
                    elif not isinstance(data, dict):
                        raise ValueError("Invalid JSON structure")
                
                processed_data = process_data(data)
                feedback = generate_feedback(processed_data)
                chart_paths = generate_charts(processed_data)
                
                # Generate PDF with unique filename
                pdf_filename = f"student_feedback_report_{report_id}.pdf"
                pdf_path = os.path.join(REPORTS_FOLDER, pdf_filename)
                generate_pdf(feedback, chart_paths, pdf_path)
                
                # Serialize processed_data for session storage
                serialized_processed_data = serialize_processed_data(processed_data)
                
                # Store report info in session
                session['report_data'] = {
                    'pdf_path': pdf_path,
                    'filename': file.filename,
                    'processed_data': serialized_processed_data,
                    'feedback_preview': feedback[:500] + "..." if len(feedback) > 500 else feedback
                }
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return redirect(url_for('preview_report'))
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return render_template('index.html', error=f"Error processing file: {str(e)}")
        else:
            return render_template('index.html', error="Invalid file format. Please upload a JSON file.")
    
    return render_template('index.html')

@app.route('/preview')
def preview_report():
    if 'report_data' not in session:
        return redirect(url_for('upload_file'))
    
    report_data = session['report_data']
    # Deserialize the processed_data
    processed_data = deserialize_processed_data(report_data['processed_data'])
    
    # Calculate some key metrics for preview
    overall = processed_data['overall']
    subjects = processed_data['subjects']
    
    # Calculate preview statistics
    preview_stats = {
        'overall_accuracy': overall['accuracy'],
        'total_marks': f"{overall['marks_scored']}/{overall['total_marks']}",
        'questions_attempted': f"{overall['attempted']}/{overall['total_questions']}",
        'time_efficiency': round((overall['time_taken'] / overall['total_time']) * 100, 1) if overall['total_time'] > 0 else 0,
        'subjects_count': len(subjects),
        'strongest_subject': max(subjects.items(), key=lambda x: x[1]['accuracy'])[0] if subjects else 'N/A',
        'weakest_subject': min(subjects.items(), key=lambda x: x[1]['accuracy'])[0] if subjects else 'N/A'
    }
    
    return render_template('preview.html', 
                         report_data=report_data, 
                         preview_stats=preview_stats)

@app.route('/download')
def download_report():
    if 'report_data' not in session:
        return redirect(url_for('upload_file'))
    
    report_data = session['report_data']
    pdf_path = report_data['pdf_path']
    
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='student_feedback_report.pdf')
    else:
        return redirect(url_for('upload_file'))

@app.route('/new-report')
def new_report():
    # Clean up old report files
    if 'report_data' in session:
        old_pdf_path = session['report_data'].get('pdf_path')
        if old_pdf_path and os.path.exists(old_pdf_path):
            try:
                os.remove(old_pdf_path)
            except:
                pass  # Ignore errors if file is already deleted
    
    # Clear session
    session.clear()
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)