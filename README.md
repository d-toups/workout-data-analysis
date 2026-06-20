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
# 1. Clone the repo
git clone https://github.com/d-toups/workout-data-analysis.git
cd workout-data-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Open the notebook
jupyter notebook notebooks/
