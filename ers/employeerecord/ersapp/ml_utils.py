import base64
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.conf import settings


MODEL_DIR = Path(settings.BASE_DIR) / 'ml'
FEATURE_COLUMNS = [
    'attendance',
    'study_hours',
    'previous_score',
    'assignments_submitted',
    'extracurricular_score',
]
MODEL_LABELS = {
    'logistic_regression': 'Logistic Regression',
    'decision_tree': 'Decision Tree',
    'random_forest': 'Random Forest',
    'knn': 'KNN',
}


def _build_training_dataframe():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(42)
    rows = []
    for _ in range(800):
        attendance = rng.uniform(40, 100)
        study_hours = rng.uniform(0.5, 10)
        previous_score = rng.uniform(30, 100)
        assignments = int(rng.integers(0, 11))
        extracurricular = rng.uniform(15, 100)
        weighted_score = (
            (attendance * 0.25) +
            (min(study_hours * 10, 100) * 0.2) +
            (previous_score * 0.35) +
            (min(assignments * 10, 100) * 0.1) +
            (extracurricular * 0.1)
        )
        if weighted_score >= 85:
            label = 'Excellent'
        elif weighted_score >= 70:
            label = 'Good'
        elif weighted_score >= 55:
            label = 'Average'
        else:
            label = 'At Risk'
        rows.append({
            'attendance': attendance,
            'study_hours': study_hours,
            'previous_score': previous_score,
            'assignments_submitted': assignments,
            'extracurricular_score': extracurricular,
            'performance_score': round(weighted_score, 2),
            'label': label,
        })
    return pd.DataFrame(rows)


def _prepare_models():
    import joblib
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    data = _build_training_dataframe()
    x_train = data[FEATURE_COLUMNS]
    y_train = data['label']

    models = {
        'logistic_regression': Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=2000)),
        ]),
        'decision_tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'random_forest': RandomForestClassifier(n_estimators=220, random_state=42),
        'knn': Pipeline([
            ('scaler', StandardScaler()),
            ('model', KNeighborsClassifier(n_neighbors=7)),
        ]),
    }

    trained = {}
    for key, model in models.items():
        model.fit(x_train, y_train)
        trained[key] = model
        joblib.dump(model, MODEL_DIR / f'{key}.joblib')
    return trained


def load_models():
    try:
        import joblib
    except Exception:
        return {}

    if not MODEL_DIR.exists():
        return _prepare_models()

    loaded = {}
    for key in MODEL_LABELS:
        model_path = MODEL_DIR / f'{key}.joblib'
        if model_path.exists():
            loaded[key] = joblib.load(model_path)
    if len(loaded) != len(MODEL_LABELS):
        return _prepare_models()
    return loaded


def _build_feature_vector(profile_data):
    return [[
        float(profile_data.get('attendance') or 0),
        float(profile_data.get('study_hours') or 0),
        float(profile_data.get('previous_score') or 0),
        float(profile_data.get('assignments_submitted') or 0),
        float(profile_data.get('extracurricular_score') or 0),
    ]]


def calculate_numeric_score(profile_data):
    attendance = float(profile_data.get('attendance') or 0)
    study_hours = float(profile_data.get('study_hours') or 0)
    previous_score = float(profile_data.get('previous_score') or 0)
    assignments = float(profile_data.get('assignments_submitted') or 0)
    extracurricular = float(profile_data.get('extracurricular_score') or 0)
    score = (
        (attendance * 0.25) +
        (min(study_hours * 10, 100) * 0.2) +
        (previous_score * 0.35) +
        (min(assignments * 10, 100) * 0.1) +
        (extracurricular * 0.1)
    )
    return Decimal(str(round(score, 2)))


def predict_student_performance(profile_data, model_choice='auto'):
    models = load_models()
    if not models:
        score = calculate_numeric_score(profile_data)
        label = 'Excellent' if score >= 85 else 'Good' if score >= 70 else 'Average' if score >= 55 else 'At Risk'
        return {
            'label': label,
            'confidence': Decimal('75.00'),
            'score': score,
            'model_key': 'auto',
            'model_name': 'Rule Based',
        }

    model_key = model_choice if model_choice in models else 'random_forest'
    if model_choice == 'auto':
        score = calculate_numeric_score(profile_data)
        model_key = 'logistic_regression' if score < 55 else 'decision_tree' if score < 70 else 'random_forest'

    model = models[model_key]
    features = _build_feature_vector(profile_data)
    predicted_label = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = Decimal(str(round(float(max(probabilities)) * 100, 2)))
    return {
        'label': predicted_label,
        'confidence': confidence,
        'score': calculate_numeric_score(profile_data),
        'model_key': model_key,
        'model_name': MODEL_LABELS.get(model_key, model_key.title()),
    }


def build_prediction_chart(profile_data, predicted_score):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception:
        return None

    labels = ['Attendance', 'Study Hours x10', 'Previous Score', 'Assignments x10', 'Activities', 'Predicted Score']
    values = [
        float(profile_data.get('attendance') or 0),
        min(float(profile_data.get('study_hours') or 0) * 10, 100),
        float(profile_data.get('previous_score') or 0),
        min(float(profile_data.get('assignments_submitted') or 0) * 10, 100),
        float(profile_data.get('extracurricular_score') or 0),
        float(predicted_score or 0),
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, values, color=['#0f4c81', '#1f7a8c', '#4cc9f0', '#f59e0b', '#34a853', '#ef4444'])
    ax.set_ylim(0, 100)
    ax.set_ylabel('Score')
    ax.set_title('Student Performance Factors')
    ax.tick_params(axis='x', rotation=20)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def build_history_chart(predictions):
    if not predictions:
        return {'labels': [], 'scores': [], 'actual_scores': []}
    ordered = list(reversed(predictions))
    return {
        'labels': [item.created_at.strftime('%d %b') for item in ordered],
        'scores': [float(item.predicted_score) for item in ordered],
        'actual_scores': [float(item.actual_score) if item.actual_score is not None else None for item in ordered],
    }


def build_admin_analytics(predictions):
    labels = ['Excellent', 'Good', 'Average', 'At Risk']
    counts = {label: 0 for label in labels}
    model_usage = {value: 0 for value in MODEL_LABELS.values()}
    for item in predictions:
        if item.predicted_label in counts:
            counts[item.predicted_label] += 1
        if item.model_used in model_usage:
            model_usage[item.model_used] += 1

    return {
        'prediction_labels': labels,
        'prediction_counts': [counts[label] for label in labels],
        'model_labels': list(model_usage.keys()),
        'model_counts': list(model_usage.values()),
    }
