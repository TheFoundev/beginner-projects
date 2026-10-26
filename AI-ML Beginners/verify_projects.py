"""Check that all 20 projects have code, data, and generated outputs.

Usage:
    python verify_projects.py
"""

from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parent
PROJECTS = BASE / "projects"

EXPECTED_OUTPUTS = {
    "01_snack_sorter": ["sample_snacks.png", "predictions.png", "confusion_matrix.png", "metrics.txt"],
    "02_lemonade_stand": ["lemonade_regression.png", "prediction.txt"],
    "03_titanic_survival": ["titanic_tree.png", "confusion_matrix.png", "rules.txt"],
    "04_spam_detective": ["top_words.png", "confusion_matrix.png", "predictions.txt"],
    "05_fruit_sorter": ["fruit_scatter.png", "confusion_matrix.png", "metrics.txt"],
    "06_exam_score": ["exam_score_regression.png", "metrics.txt"],
    "07_car_price": ["actual_vs_predicted.png", "metrics.txt"],
    "08_pizza_price": ["actual_vs_predicted.png", "quotes.txt"],
    "09_height_predictor": ["height_regression.png", "metrics.txt"],
    "10_sleep_screen_time": ["sleep_regression.png", "metrics.txt"],
    "11_exam_pass_predictor": ["decision_boundary.png", "confusion_matrix.png", "metrics.txt"],
    "12_fake_review_spotter": ["top_words.png", "confusion_matrix.png", "predictions.txt"],
    "13_penguin_detective": ["penguin_scatter.png", "confusion_matrix.png", "metrics.txt"],
    "14_iris_identifier": ["iris_tree.png", "confusion_matrix.png", "rules.txt"],
    "15_pumpkin_seed_sorter": ["pumpkin_tree.png", "confusion_matrix.png", "rules.txt"],
    "16_movie_mood_ring": ["mood_meter.png", "confusion_matrix.png", "predictions.txt"],
    "17_subject_chatbot": ["chatbot_tree.png", "rules.txt"],
    "18_recipe_recommender": ["similarity_scores.png", "recommendations.txt"],
    "19_news_topic_sorter": ["confusion_matrix.png", "predictions.txt"],
    "20_study_buddy_planner": ["study_tree.png", "confusion_matrix.png", "rules.txt"],
}


def main() -> int:
    problems = []
    for folder, outputs in EXPECTED_OUTPUTS.items():
        project = PROJECTS / folder
        main_file = project / "main.py"
        readme = project / "README.md"
        data = project / "data"

        if not main_file.exists():
            problems.append(f"missing code: {main_file.relative_to(BASE)}")
        if not readme.exists():
            problems.append(f"missing README: {readme.relative_to(BASE)}")
        if not data.exists() or not any(data.iterdir()):
            problems.append(f"missing data: {data.relative_to(BASE)}")
        for output in outputs:
            path = project / "outputs" / output
            if not path.exists():
                problems.append(f"missing output: {path.relative_to(BASE)}")

    if problems:
        print("Problems found:")
        for problem in problems:
            print(f"  - {problem}")
        print("\nRun `python run_all.py` to generate missing outputs.")
        return 1

    print(f"OK: {len(EXPECTED_OUTPUTS)} projects have code, data, README, and outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
