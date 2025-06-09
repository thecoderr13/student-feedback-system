import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from collections import defaultdict

def generate_charts(processed_data):
    """
    Generate charts for the report using Plotly.

    Args:
        processed_data (dict): Processed data containing performance metrics.

    Returns:
        dict: Dictionary of chart names to their file paths.
    """
    # Create a directory for saving charts if it doesn't exist
    if not os.path.exists('charts'):
        os.makedirs('charts')

    # Initialize dictionary to store chart file paths
    chart_paths = {}

    # Color scheme for consistency
    colors = {
        'correct': '#2ecc71',  # Green
        'incorrect': '#e74c3c',  # Red
        'unattempted': '#95a5a6',  # Grey
        'low': '#e74c3c',  # Red for <40%
        'medium': '#f1c40f',  # Yellow for 40-70%
        'high': '#2ecc71',  # Green for >70%
    }

    # Helper function to determine performance color based on percentage
    def get_performance_color(value):
        if value < 40:
            return colors['low']
        elif value <= 70:
            return colors['medium']
        else:
            return colors['high']

    # --- Chart 1: Subject-wise Accuracy Bar Chart (Updated from Original) ---
    subjects = list(processed_data['subjects'].keys())
    accuracies = [processed_data['subjects'][sub]['accuracy'] for sub in subjects]
    subject_accuracy_fig = px.bar(
        x=subjects, y=accuracies,
        title="Subject-Wise Accuracy",
        labels={'x': 'Subject', 'y': 'Accuracy (%)'},
        color=accuracies,
        color_continuous_scale=[colors['low'], colors['medium'], colors['high']]
    )
    subject_accuracy_path = 'charts/subject_accuracy.png'
    subject_accuracy_fig.write_image(subject_accuracy_path)
    chart_paths['Subject-Wise Accuracy'] = subject_accuracy_path

    # --- Chart 2: Difficulty-wise Attempt Distribution Pie Chart (Updated from Original) ---
    difficulties = list(processed_data['difficulty_metrics'].keys())
    attempted_counts = [processed_data['difficulty_metrics'][d]['attempted'] for d in difficulties]
    difficulty_distribution_fig = px.pie(
        names=difficulties,
        values=attempted_counts,
        title="Difficulty-Wise Attempt Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    difficulty_distribution_path = 'charts/difficulty_distribution.png'
    difficulty_distribution_fig.write_image(difficulty_distribution_path)
    chart_paths['Difficulty-Wise Attempt Distribution'] = difficulty_distribution_path

    # --- Chart 3: Overall Attempt Status Pie Chart (Correct, Incorrect, Unattempted) ---
    overall = processed_data['overall']
    total_questions = overall['total_questions']
    correct = overall['correct']
    attempted = overall['attempted']
    incorrect = attempted - correct
    unattempted = total_questions - attempted
    attempt_status_fig = px.pie(
        names=['Correct', 'Incorrect', 'Unattempted'],
        values=[correct, incorrect, unattempted],
        title="Overall Attempt Status Distribution",
        color_discrete_map={
            'Correct': colors['correct'],
            'Incorrect': colors['incorrect'],
            'Unattempted': colors['unattempted']
        }
    )
    attempt_status_path = 'charts/attempt_status_distribution.png'
    attempt_status_fig.write_image(attempt_status_path)
    chart_paths['Overall Attempt Status Distribution'] = attempt_status_path

    # --- Chart 4: Subject-wise Marks Scored Bar Chart ---
    marks = [processed_data['subjects'][sub]['marks_scored'] for sub in subjects]
    marks_fig = px.bar(
        x=subjects, y=marks,
        title="Subject-Wise Marks Scored",
        labels={'x': 'Subject', 'y': 'Marks Scored'},
        color=marks,
        color_continuous_scale=[colors['low'], colors['medium'], colors['high']]
    )
    marks_path = 'charts/subject_marks.png'
    marks_fig.write_image(marks_path)
    chart_paths['Subject-Wise Marks Scored'] = marks_path

    # --- Chart 5: Time Distribution Across Subjects (Pie Chart) ---
    time_taken = [processed_data['subjects'][sub]['time_taken'] / 60 for sub in subjects]  # Convert to minutes
    time_dist_fig = px.pie(
        names=subjects,
        values=time_taken,
        title="Time Distribution Across Subjects (Minutes)",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    time_dist_path = 'charts/time_distribution.png'
    time_dist_fig.write_image(time_dist_path)
    chart_paths['Time Distribution Across Subjects'] = time_dist_path

    # --- Chart 6: Difficulty-wise Accuracy Bar Chart ---
    difficulty_data = pd.DataFrame([
        {'Difficulty': diff, 'Accuracy': metrics['accuracy']}
        for diff, metrics in processed_data['difficulty_metrics'].items()
    ])
    diff_accuracy_fig = px.bar(
        difficulty_data, x='Difficulty', y='Accuracy',
        title="Difficulty-Wise Accuracy",
        color='Accuracy',
        color_continuous_scale=[colors['low'], colors['medium'], colors['high']]
    )
    diff_accuracy_path = 'charts/difficulty_accuracy.png'
    diff_accuracy_fig.write_image(diff_accuracy_path)
    chart_paths['Difficulty-Wise Accuracy'] = diff_accuracy_path

    # --- Chart 7: Chapter-wise Accuracy Bar Chart ---
    chapter_data = pd.DataFrame([
        {'Subject': sub, 'Chapter': chap, 'Accuracy': metrics['accuracy']}
        for (sub, chap), metrics in processed_data['chapter_metrics'].items()
    ])
    chapter_fig = px.bar(
        chapter_data, x='Chapter', y='Accuracy', color='Subject',
        title="Chapter-Wise Accuracy",
        barmode='group'
    )
    chapter_path = 'charts/chapter_accuracy.png'
    chapter_fig.write_image(chapter_path)
    chart_paths['Chapter-Wise Accuracy'] = chapter_path

   # --- Chart 8: Concept-wise Accuracy Scatter Plot (Vertical) ---
    concept_data = pd.DataFrame([
        {'Subject': sub, 'Concept': concept, 'Accuracy': metrics['accuracy'], 'Attempted': metrics['attempted']}
        for (sub, concept), metrics in processed_data['concept_metrics'].items()
    ])
    concept_fig = px.scatter(
        concept_data, x='Accuracy', y='Concept', color='Subject', size='Attempted',
        title="Concept-Wise Accuracy Breakdown"
    )
    # Rotate x-axis labels for better readability
    concept_fig.update_layout(
        xaxis_title="Accuracy (%)",
        yaxis_title="Concept",
        xaxis=dict(tickangle=0),
        yaxis=dict(tickangle=0),
        margin=dict(l=150, r=50, t=50, b=50)  # Adjust left margin for long concept names
    )
    concept_path = 'charts/concept_accuracy.png'
    concept_fig.write_image(concept_path)
    chart_paths['Concept-Wise Accuracy'] = concept_path

    # --- Chart 9: Time vs Performance Scatter Plot (Subject-wise) ---
    subject_df = pd.DataFrame({
        'Subject': subjects,
        'Marks Scored': [processed_data['subjects'][sub]['marks_scored'] for sub in subjects],
        'Time Taken (min)': [processed_data['subjects'][sub]['time_taken'] / 60 for sub in subjects],
        'Accuracy': accuracies
    })
    time_performance_fig = px.scatter(
        subject_df, x='Time Taken (min)', y='Marks Scored', color='Subject', size='Accuracy',
        title="Time vs Performance Across Subjects"
    )
    time_performance_path = 'charts/time_vs_performance.png'
    time_performance_fig.write_image(time_performance_path)
    chart_paths['Time vs Performance'] = time_performance_path

    # --- Chart 10: Time per Question Scatter Plot ---
    questions_df = pd.DataFrame(processed_data['questions_data'])
    questions_df['Question Number'] = range(1, len(questions_df) + 1)
    time_per_question_fig = px.scatter(
        questions_df, x='Question Number', y='time_taken', color='correct',
        title="Time per Question",
        color_discrete_map={True: colors['correct'], False: colors['incorrect']},
        labels={'time_taken': 'Time Taken (sec)'}
    )
    time_per_question_path = 'charts/time_per_question.png'
    time_per_question_fig.write_image(time_per_question_path)
    chart_paths['Time per Question'] = time_per_question_path

    return chart_paths