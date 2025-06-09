from collections import defaultdict

def get_subject_from_title(title):
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in ['physics', 'phys']):
        return 'Physics'
    elif any(keyword in title_lower for keyword in ['chemistry', 'chem']):
        return 'Chemistry'
    elif any(keyword in title_lower for keyword in ['mathematics', 'math', 'maths']):
        return 'Mathematics'
    return 'Unknown'

def process_data(data, subject_map=None):
    if subject_map is None:
        subject_map = {
            "607018ee404ae53194e73d92": "Physics",
            "607018ee404ae53194e73d90": "Chemistry",
            "607018ee404ae53194e73d91": "Mathematics"
        }

    if isinstance(data, list):
        data = data[0] if data else {}
    elif not isinstance(data, dict):
        raise ValueError("Invalid JSON structure: expected a list or dictionary")

    overall = {
        'marks_scored': data.get('totalMarkScored', 0),
        'total_marks': data.get('test', {}).get('totalMarks', 0),
        'attempted': data.get('totalAttempted', 0),
        'total_questions': data.get('test', {}).get('totalQuestions', 0),
        'correct': data.get('totalCorrect', 0),
        'accuracy': data.get('accuracy', 0),
        'time_taken': data.get('totalTimeTaken', 0),
        'total_time': data.get('test', {}).get('totalTime', 0) * 60  # Convert minutes to seconds
    }

    subjects = {}
    for sub in data.get('subjects', []):
        sub_id = sub.get('subjectId', {}).get('$oid', 'Unknown')
        sub_name = subject_map.get(sub_id, 'Unknown')
        subjects[sub_name] = {
            'marks_scored': sub.get('totalMarkScored', 0),
            'total_marks': 100,  # Hardcoded due to lack of per-question marks
            'attempted': sub.get('totalAttempted', 0),
            'correct': sub.get('totalCorrect', 0),
            'accuracy': sub.get('accuracy', 0),
            'time_taken': sub.get('totalTimeTaken', 0)
        }

    chapter_performance = defaultdict(lambda: {'attempted': 0, 'correct': 0, 'time_taken': 0})
    difficulty_performance = defaultdict(lambda: {'attempted': 0, 'correct': 0, 'time_taken': 0})
    concept_performance = defaultdict(lambda: {'attempted': 0, 'correct': 0, 'time_taken': 0})
    questions_data = []

    sections = data.get('sections', [])
    for section in sections:
        section_id = section.get('sectionId', {})
        title = section_id.get('title', '')
        subject = get_subject_from_title(title)
        questions = section.get('questions', [])
        for question in questions:
            q_data = question.get('questionId', {})
            chapter = q_data.get('chapters', [{}])[0].get('title', 'Unknown')
            difficulty = q_data.get('level', 'Unknown')
            concepts = [c.get('title', 'Unknown') for c in q_data.get('concepts', [])]
            time_taken = question.get('timeTaken', 0)

            marked_options = question.get('markedOptions', [])
            input_value = question.get('inputValue', {})
            if marked_options:
                attempted = len(marked_options) > 0
                correct = any(opt.get('isCorrect', False) for opt in marked_options) if attempted else False
            elif input_value:
                attempted = input_value.get('value') is not None
                correct = input_value.get('isCorrect', False) if attempted else False
            else:
                attempted = False
                correct = False

            if attempted:
                chapter_key = (subject, chapter)
                chapter_performance[chapter_key]['attempted'] += 1
                chapter_performance[chapter_key]['time_taken'] += time_taken
                difficulty_performance[difficulty]['attempted'] += 1
                difficulty_performance[difficulty]['time_taken'] += time_taken
                for concept in concepts:
                    concept_key = (subject, concept)
                    concept_performance[concept_key]['attempted'] += 1
                    concept_performance[concept_key]['time_taken'] += time_taken
                if correct:
                    chapter_performance[chapter_key]['correct'] += 1
                    difficulty_performance[difficulty]['correct'] += 1
                    for concept in concepts:
                        concept_key = (subject, concept)
                        concept_performance[concept_key]['correct'] += 1

            questions_data.append({
                'subject': subject,
                'chapter': chapter,
                'difficulty': difficulty,
                'concepts': concepts,
                'attempted': attempted,
                'correct': correct,
                'time_taken': time_taken
            })

    def calculate_metrics(perf_dict):
        metrics = {}
        for key, perf in perf_dict.items():
            attempted = perf['attempted']
            if attempted > 0:
                accuracy = (perf['correct'] / attempted) * 100
                avg_time = perf['time_taken'] / attempted
            else:
                accuracy = 0
                avg_time = 0
            metrics[key] = {
                'attempted': attempted,
                'correct': perf['correct'],
                'accuracy': accuracy,
                'avg_time': avg_time
            }
        return metrics

    chapter_metrics = calculate_metrics(chapter_performance)
    difficulty_metrics = calculate_metrics(difficulty_performance)
    concept_metrics = calculate_metrics(concept_performance)

    correct_times = [q['time_taken'] for q in questions_data if q['attempted'] and q['correct']]
    incorrect_times = [q['time_taken'] for q in questions_data if q['attempted'] and not q['correct']]
    avg_time_correct = sum(correct_times) / len(correct_times) if correct_times else 0
    avg_time_incorrect = sum(incorrect_times) / len(incorrect_times) if incorrect_times else 0

    return {
        'overall': overall,
        'subjects': subjects,
        'chapter_metrics': chapter_metrics,
        'difficulty_metrics': difficulty_metrics,
        'concept_metrics': concept_metrics,
        'avg_time_correct': avg_time_correct,
        'avg_time_incorrect': avg_time_incorrect,
        'questions_data': questions_data
    }