# Workout Data Analysis: Gender & Age Differences in Fitness Preferences & Calorie Burn

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14pcN7JquS_n7Ydf5GZy8UZV7MxNn0HkY)

**Exploratory Data Analysis** of workout preferences and calorie expenditure patterns across gender and age groups.

## Project Objective
Analyze how **workout type preferences** and **training intensity** (Calories Per Minute) vary by gender and age group to derive actionable insights for fitness apps, gyms, and wellness platforms.

## Key Business Questions
- Do workout preferences differ significantly between males and females?
- How does training intensity vary across age groups and genders?
- What patterns can inform personalized fitness recommendations?

## Tech Stack
- Python
- pandas
- seaborn + matplotlib
- scipy (statistical testing)

## Repository Structure
```text
workout-data-analysis/
├── notebooks/
│   └── workout_data_eda.ipynb                 ← Main analysis notebook
├── src/
│   └── workout_data_analysis.py                    ← Clean Python functions
├── reports/
│   └── figures/                               ← Saved visualizations
├── data/
├── requirements.txt
├── README.md
└── LICENSE
```

## How to Run

```bash
# Clone the repository
git clone https://github.com/d-toups/workout-data-analysis.git
cd workout-data-analysis

# Install dependencies
pip install -r requirements.txt

# Open the notebook
jupyter notebook notebooks/
```
Or simply click the "Open in Colab" badge above.

## Results Visualizations

**Male Workout Preferences**
![Male Preferences](reports/figures/male_workout_type_pref.png)

**Female Workout Preferences**
![Female Preferences](reports/figures/female_workout_type_pref.png)

**Calories Burned per Minute**
![CPM](reports/figures/cpm.png)

## Key Insights
- **Gender Preferences**: Males consistently prefer **Strength Training** and **HIIT**, while females show stronger preference for **Cardio** and **Yoga**.
- **Age Patterns**: Young Adults tend to train at higher intensity (Calories Per Minute) compared to Adults across several workout types.
- **Strength Training** shows the highest variability in intensity, particularly among males, with several high outliers suggesting diverse training efforts within this category.
- **Notable Reversal in Females**: Adult females prefer Cardio most and Yoga least, while Young Adult females show the opposite pattern (Yoga most preferred, Cardio least).
- **Statistical Results**: Stratified Chi-square and T-tests found **no statistically significant differences** between genders or age groups (all p-values > 0.05).

## Conclusions & Business Recommendations
**Main Findings**  
Visual analysis reveals clear behavioral patterns: males lean toward higher-intensity workouts (Strength Training and HIIT), while females prefer Cardio and Yoga. Young Adults also demonstrate higher training intensity compared to Adults in several categories. Strength Training stands out for its wide range of intensity, especially among males.

However, statistical testing (Chi-square and T-tests) showed **no significant differences** between groups. This suggests that while visual trends are present, they are not strong enough to be considered statistically meaningful with this dataset.

**Business Implications**  
Fitness apps and gyms can use these visual patterns to offer **soft personalization** — such as recommending more Strength and CrossFit options to young males, or promoting Yoga and Cardio to females. Strong demographic-based assumptions should be made cautiously and validated with larger datasets.

**Limitations**  
- Seniors were excluded due to very small and non-representative sample size.
- The dataset is synthetic, which may limit real-world generalizability.
- Moderate sample size likely contributed to the non-significant statistical results.

## Future Work
- Analyze a larger, real-world dataset
- Perform regression analysis to control for multiple variables
