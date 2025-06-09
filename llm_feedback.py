import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_feedback(processed_data):
    """Generate personalized feedback using Gemini API.

    Args:
        processed_data (dict): Processed data containing performance metrics.

    Returns:
        str: Markdown-formatted feedback.
    """
    # Prepare context
    context = "### Test Performance Data\n\n"
    
    # Overall Performance
    overall = processed_data['overall']
    context += "#### Overall Performance\n"
    context += f"- Marks: {overall['marks_scored']} / {overall['total_marks']}\n"
    context += f"- Questions Attempted: {overall['attempted']} / {overall['total_questions']}\n"
    context += f"- Correct Answers: {overall['correct']} / {overall['attempted']}\n"
    context += f"- Accuracy: {overall['accuracy']:.2f}%\n"
    context += f"- Time Taken: {overall['time_taken']} sec / {overall['total_time']} sec\n\n"

    # Subject-wise Performance
    context += "#### Subject-wise Performance\n"
    for sub, metrics in processed_data['subjects'].items():
        context += f"- **{sub}**:\n"
        context += f"  - Marks: {metrics['marks_scored']} / {metrics['total_marks']}\n"
        context += f"  - Attempted: {metrics['attempted']}\n"
        context += f"  - Correct: {metrics['correct']}\n"
        context += f"  - Accuracy: {metrics['accuracy']:.2f}%\n"
        context += f"  - Time Taken: {metrics['time_taken']} sec\n"

    # Chapter-wise Performance
    context += "#### Chapter-wise Performance\n"
    for (sub, chap), metrics in processed_data['chapter_metrics'].items():
        context += f"- **{sub} - {chap}**:\n"
        context += f"  - Attempted: {metrics['attempted']}\n"
        context += f"  - Correct: {metrics['correct']}\n"
        context += f"  - Accuracy: {metrics['accuracy']:.2f}%\n"
        context += f"  - Avg Time per Question: {metrics['avg_time']:.2f} sec\n"

    # Difficulty-wise Performance
    context += "#### Difficulty-wise Performance\n"
    for diff, metrics in processed_data['difficulty_metrics'].items():
        context += f"- **{diff}**:\n"
        context += f"  - Attempted: {metrics['attempted']}\n"
        context += f"  - Correct: {metrics['correct']}\n"
        context += f"  - Accuracy: {metrics['accuracy']:.2f}%\n"
        context += f"  - Avg Time per Question: {metrics['avg_time']:.2f} sec\n"

    # Concept-wise Performance
    context += "#### Concept-wise Performance\n"
    for (sub, concept), metrics in processed_data['concept_metrics'].items():
        context += f"- **{sub} - {concept}**:\n"
        context += f"  - Attempted: {metrics['attempted']}\n"
        context += f"  - Correct: {metrics['correct']}\n"
        context += f"  - Accuracy: {metrics['accuracy']:.2f}%\n"
        context += f"  - Avg Time per Question: {metrics['avg_time']:.2f} sec\n"

    # Time vs Accuracy Insights
    context += "#### Time vs Accuracy Insights\n"
    context += f"- Avg Time on Correct Answers: {processed_data['avg_time_correct']:.2f} sec\n"
    context += f"- Avg Time on Incorrect Answers: {processed_data['avg_time_incorrect']:.2f} sec\n"

    # LLM Prompt
    prompt = f"""
You are an expert academic coach tasked with generating a personalized feedback report for a student based on their test performance. Using the data below, create a report that includes:

1. **Introduction**: A warm, motivating, and highly personalized message reflecting the student's specific performance (e.g., strengths in Physics, struggles in Mathematics). Avoid generic phrases.
2. **Performance Breakdown**: Detailed insights at overall, subject, chapter, difficulty, and concept levels. Highlight key patterns (e.g., strong/weak areas).
3. **Time vs Accuracy Insights**: Analyze how time management impacts performance, referencing specific metrics.
4. **Actionable Suggestions**: Provide 2-3 specific, tailored suggestions for improvement based on the data.

Format your response in Markdown with clear headings and bullet points. Ensure the tone is encouraging, professional, and human-like, with specific references to the data.

**Test Data:**
{context}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating feedback: {str(e)}"