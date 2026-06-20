# Workout Data Analysis: Gender & Age Differences in Fitness Preferences & Calorie Burn

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z2Zam_9rwGqDvOR6YE06Fj4Zea51iGgE)

**Exploratory Data Analysis** of workout preferences and calorie expenditure across gender and age groups.

## Project Objective
Explore how workout type preferences and calorie burn intensity vary by **gender** and **age group** to derive actionable insights for fitness apps, gyms, and wellness platforms.

## Key Business Questions
- Do men and women prefer different workout types?
- How does workout intensity (calories per minute) differ by gender and age?
- What patterns emerge that could inform personalized fitness recommendations?

## Tech Stack
- **Python**  
- **pandas** – data cleaning & manipulation  
- **seaborn + matplotlib** – visualization  
- **scipy** – statistical testing  

## Repository Structure
workout-data-analysis/
├── notebooks/
│   └── workout_data_eda.ipynb          ← Main analysis notebook
├── src/
│   └── workout_data_analysis.py        ← Python script version
├── data/
├── reports/
│   └── figures/                        ← Saved visualizations
├── requirements.txt
├── README.md
└── LICENSE

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/d-toups/workout-data-analysis.git
cd workout-data-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Jupyter Notebook
jupyter notebook notebooks/
```
Or simply click the "Open in Colab" badge above.

## Key Insights
- **Gender Preferences**: Males strongly favor **Strength** training and **HIIT**, while females prefer **Cardio** and **Yoga**.
- **Intensity (Calories Per Minute)**: Young adults (18-34) show the highest intensity, especially males.
- **Statistical Significance**:
  - Chi-square test confirmed a strong association between gender and workout type preference (**p < 0.05**).
  - Males have significantly higher calories per minute than females (independent t-test).

## Conclusions & Business Recommendations
- Fitness platforms should personalize workout suggestions based on **gender + age**.
- Gyms can optimize class schedules (e.g., more Strength/HIIT for young males, more Cardio/Yoga for females).
- Age-based intensity expectations can improve goal setting in wellness apps.

## Limitations
- Small senior sample size (only 15 records, all age 65) → potential selection bias.
- Dataset likely comes from self-reported/app-tracked workouts (may over-represent motivated individuals).

## Future Work
- Statistical power analysis and more robust testing
- Predictive modeling for calorie burn
- Interactive dashboard (Streamlit / Plotly Dash)
- Expand dataset with more diverse age groups
