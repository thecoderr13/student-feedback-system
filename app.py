from flask import Flask, request, send_file, render_template
import os
from data_processing import process_data
from llm_feedback import generate_feedback
from chart_generator import generate_charts
from pdf_generator import generate_pdf
import json

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            # Process the uploaded JSON file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)[0]  # Assuming the JSON is a list with one element
            processed_data = process_data(data)
            feedback = generate_feedback(processed_data)
            chart_paths = generate_charts(processed_data)
            pdf_path = generate_pdf(feedback, chart_paths)
            # Clean up uploaded file
            os.remove(filepath)
            return send_file(pdf_path, as_attachment=True, download_name='student_feedback_report.pdf')
        else:
            return "Invalid file format. Please upload a JSON file."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)