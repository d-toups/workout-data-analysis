# Workout Data Analysis

**Explore how workout preferences and calorie expenditure differ by gender and age group.**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/d-toups/workout-data-analysis/blob/main/notebooks/workout_data_eda.ipynb)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Pandas](https://img.shields.io/badge/pandas-2.0+-blue)
![Seaborn](https://img.shields.io/badge/seaborn-0.13+-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## Objective
Analyze workout preferences, training intensity, and demographic patterns using exploratory data analysis, statistical testing, and predictive modeling.

## Key Business Questions
- Do workout preferences differ by gender?
- How does training intensity vary across age groups?
- What patterns can inform personalized fitness recommendations?

## Key Results
- Both males and females show a general preference for **Strength Training** and **Cardio**.
- **Young Adult males** have the strongest preference for **Yoga** among all groups (likely influenced by dataset selection bias).
- Young Adults (18-34) train at **significantly higher intensity** than Adults (35-59) for both genders (p < 0.001).
- Predictive modeling performed best for **Experience Level** (0.84 accuracy).

## Tech Stack
- Python (pandas, seaborn, matplotlib, scikit-learn, xgboost)
- Jupyter Notebook
- GitHub

## Repository Structure
```bash
workout-data-analysis/
├── main.py                             # Main execution script
├── data_loader.py
├── feature_engineering.py
├── eda.py
├── feature_selection.py
├── modeling.py
├── utils.py
├── gym_members_exercise_tracking.csv   # Raw dataset
├── notebooks/
│   └── workout_data_analysis.ipynb     # Main analysis notebook
├── reports/
│   └── figures/                        ← Saved visualizations
├── data/
├── requirements.txt
├── README.md
└── LICENSE
```

## How to Reproduce

```bash
# Clone the repository
git clone https://github.com/d-toups/workout-data-analysis.git
cd workout-data-analysis

# Install dependencies
pip install -r requirements.txt

# Open the notebook
jupyter notebook notebooks/workout_data_eda.ipynb
```
Or simply click the "Open in Colab" badge above.

## Results Visualizations

**Male Workout Preferences**
![Male Preferences](reports/figures/male_workout_type_pref.png)

**Female Workout Preferences**
![Female Preferences](reports/figures/female_workout_type_pref.png)

**Calories Burned per Minute**
![CPM](reports/figures/cpm.png)

## Modeling Results

| Target                  | Best Model | Accuracy |
|-------------------------|------------|----------|
| Experience Level        | XGBoost    | 0.84     |
| Age Group               | XGBoost    | 0.70     |
| Body Fat Group          | XGBoost    | 0.63     |

## Business Value
These insights can help fitness apps, gyms, and wellness platforms create more targeted programs and personalized recommendations based on age and training intensity.

## Conclusions & Key Insights
- **Workout Preferences**: Both genders favor Strength Training and Cardio overall. Young Adult males stand out with a particularly strong preference for Yoga.
- **Training Intensity**: Age is a much stronger driver than gender — Young Adults train significantly harder than Adults (highly significant t-tests).
- Statistical tests confirm that while visual patterns exist, gender-based workout type differences are **not statistically significant**.
**Business Takeaway**: Prioritize age over gender when personalizing workout **intensity**. Gender can still guide soft recommendations for workout types.

## Limitations
- Moderate sample size (~973 records) limits statistical power for some tests.
- No data available for individuals aged 60+.
- No multiple comparison correction was applied to the t-tests.

## Future Work
- Incorporate additional features (goals, motivation, injury history)
- Deploy models as a simple web app
- Expand analysis with larger datasets
