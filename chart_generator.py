import matplotlib.pyplot as plt
import os

def generate_charts(processed_data):
    """
    Generate charts for the report.

    Args:
        processed_data (dict): Processed data containing performance metrics.

    Returns:
        dict: Dictionary of chart names to their file paths.
    """
    chart_paths = {}

    # Subject-wise Accuracy Bar Chart
    subjects = list(processed_data['subjects'].keys())
    accuracies = [processed_data['subjects'][sub]['accuracy'] for sub in subjects]
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, accuracies, color='skyblue')
    plt.title("Subject-Wise Accuracy")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)
    subject_accuracy_path = 'subject_accuracy.png'
    plt.savefig(subject_accuracy_path)
    plt.close()
    chart_paths['Subject-Wise Accuracy'] = subject_accuracy_path

    # Difficulty-wise Attempt Distribution Pie Chart
    difficulties = list(processed_data['difficulty_metrics'].keys())
    attempted_counts = [processed_data['difficulty_metrics'][d]['attempted'] for d in difficulties]
    plt.figure(figsize=(6, 6))
    plt.pie(attempted_counts, labels=difficulties, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral', 'lightskyblue'])
    plt.title("Difficulty-Wise Attempt Distribution")
    difficulty_distribution_path = 'difficulty_distribution.png'
    plt.savefig(difficulty_distribution_path)
    plt.close()
    chart_paths['Difficulty-Wise Attempt Distribution'] = difficulty_distribution_path

    return chart_paths