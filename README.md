# EduAnalysis - Student Performance Feedback Report Generator 

A Flask-based web application that processes student test performance data, generates personalized feedback using Google Gemini API, creates visualizations, and produces comprehensive PDF reports with actionable insights.

## Features

- **Automated Data Processing**: Parses JSON test data to extract comprehensive performance metrics
- **AI-Powered Feedback**: Generates personalized feedback using Google Gemini API
- **Dynamic Visualizations**: Creates interactive charts using Plotly for performance analysis
- **PDF Report Generation**: Produces structured reports with ReportLab integration
- **Web Interface**: User-friendly Flask application for file upload and report generation

## Tech Stack

- **Backend**: Flask, Python
- **AI Integration**: Google Gemini API (gemini-1.5-flash)
- **Data Visualization**: Plotly, Pandas
- **PDF Generation**: ReportLab
- **File Processing**: JSON parsing with comprehensive data extraction

## Report Structure

The generated PDF report includes:

1. **Introduction & Overview**: Personalized motivational message with performance highlights
2. **Performance Analysis**: 
   - Overall performance metrics
   - Subject-wise breakdown
   - Chapter-wise analysis
   - Difficulty-level insights
   - Concept-wise performance
3. **Time Management Analysis**: Time vs accuracy correlation insights
4. **Actionable Recommendations**: Data-driven suggestions for improvement
5. **Visual Analytics**: Comprehensive charts and graphs on separate pages

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student-performance-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your-google-api-key" > .env
   ```

5. **Install system dependencies** (for chart rendering)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0
   
   # macOS
   brew install cairo pango
   ```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Navigate to `http://localhost:5000`
   - Upload JSON test data file
   - Preview generated statistics
   - Download comprehensive PDF report

## API Integration

### Google Gemini API
The application leverages Google's Gemini 1.5 Flash model for generating contextual, personalized feedback. The AI analyzes performance patterns and provides:

- Personalized introductions highlighting strengths and improvement areas
- Detailed performance breakdowns across multiple dimensions
- Time management insights and recommendations
- Actionable, data-driven suggestions for academic improvement

## Dependencies

```
Flask==2.3.2 
google-generativeai==0.7.2 
matplotlib==3.7.1 
reportlab==4.2.2
markdown==3.4.3
python-dotenv>=1.0.1
pandas==2.2.2 
kaleido==0.2.1
gunicorn==22.0.0

```

## Configuration

### Environment Variables
```env
GOOGLE_API_KEY=your-google-gemini-api-key
SECRET_KEY=your-secret-key-for-dev

```

### API Key Setup
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Gemini API
3. Create credentials and obtain your API key
4. Add the key to your `.env` file

## Data Format

The application expects JSON input with the following structure:
- Overall performance metrics
- Subject-wise breakdown
- Individual question details with chapters, difficulty levels, and concepts
- Time tracking data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate documentation.

---

**Thank you for using Student Performance Feedback Report Generator!** 

Hoping this tool helps educators and students gain valuable insights into academic performance.



