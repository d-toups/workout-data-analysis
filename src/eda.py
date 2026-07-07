'''
Author: Dennis Toups
Date: 6 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
import warnings; warnings.filterwarnings('ignore')

# Standardize plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

RANDOM_STATE = 42
TEST_SIZE = 0.2
NEIGHBORS = 6

################### Function Definition #######################################

""" Plot Functions ************************************************************
Purpose: Generate visualizations to illustrate insights from the dataset.

Inputs: workout dataframe
    
Outputs: Misc plots illustrating workout preferences among age groups by
gender and vice versa.

----------------------------------------------------------------------------"""

def plot_workout_by_age_group(df_in):
    # Set style
    sns.set_style("whitegrid")
    colors = sns.color_palette("Set2")
    
    for gender in ['Male', 'Female']:
        df = df_in[df_in['Gender'] == gender]
        crosstab_age = pd.crosstab(df['Age Group'], df['Workout Type'],
                                   normalize='index') * 100
        ax = crosstab_age.plot(kind='bar', color=colors, width=0.7)
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3)
        
        # Add horizontal mean line
        mean_value = crosstab_age.values.mean()
        ax.axhline(y=mean_value, color='red', linestyle='--', linewidth=2, \
                   label=f'Overall Mean ({mean_value:.1f}%)')
            
        # Add sample size annotation (n=xxx) below the legend
        sample_sizes = df['Age Group'].value_counts().sort_index()    
        text = "\n".join([f"{age}: n={count}" for age, count in 
                          sample_sizes.items()])
        plt.figtext(0.92, 0.15, text, fontsize=11, 
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
            
        plt.title(f'{gender} Workout Type Preference by Age Group (%)',
                  fontsize=14, pad=20)
        plt.ylabel('Percentage of Workouts')
        plt.xlabel('Age Group')
        plt.xticks(rotation=0)
        plt.legend(title='Workout Type', bbox_to_anchor=(1.05, 1),
                   loc='upper left')
        plt.tight_layout()
        #plt.savefig('../reports/figures/workout_type_by_age.png', dpi=300,
            #bbox_inches='tight')
        plt.show()
        plt.close()
    
    return 

def plot_cpm (df):
    # CPM by Workout Type, split by Age Group and Gender
    sns.catplot(
        data=df, 
        x='Workout Type', 
        y='Calories Per Minute',
        hue='Gender',
        col='Age Group',
        kind='box',
        height=5,
        aspect=1.1,
        palette='Set2',
        showfliers=False
        )

    plt.suptitle('Calories Per Minute by Workout Type, Age Group, and Gender', y=1.05)
    plt.xticks(rotation=45)
    plt.show()
    plt.close()
    
    return

""" Stats and Correlations ****************************************************
Purpose: Run statistical testing to find correlations in the dataset. Plot 
correlation heatmap to further investigate correlations to aid in avoiding data 
leakage during feature selection.

Inputs: df - dataframe containing dataset
    
Outputs: Generates chi-square and T-test results and delivers determination 
of any associations within the dataset, as well as correlation heat map.
----------------------------------------------------------------------------"""

def stats(df):
    results = []
    
    # Get all numerical columns
    numerical_cols = df.select_dtypes(include='number').columns.tolist()
    
    # Chi-Square Test Workout Type vs. Gender by Age Group
    print('\n--------- Chi square tests  ---------\n')
    for age_group in sorted(df['Age Group'].unique()):
        subset = df[df['Age Group'] == age_group]
        contingency = pd.crosstab(subset['Gender'], subset['Workout Type'])
        
        if contingency.shape[0] >= 2 and contingency.shape[1] >= 2:
            chi2, p, _, _ = chi2_contingency(contingency)
            results.append({
                'Test': 'Chi-square',
                'Group': f'Age Group: {age_group}',
                'Comparison': 'Gender vs Workout Type',
                'p-value': round(p, 4),
                'Significant': p < 0.05
            })
            
        print(f"Age Group: {age_group} ({len(subset)} samples)")
        print(f"   Chi-square p-value: {p:.4f} → {'Significant' if \
              p < 0.05 else 'Not significant'}")
        print(f"   Contingency Table:\n{contingency}")
        
    # T-tests by Age Group within Gender
    print('\n--------- T-tests by age group within each gender ---------')
    for gender in ['Male', 'Female']:
        subset = df[df['Gender'] == gender]
        
        for label in numerical_cols:
            young = subset[subset['Age Group'] == 'Young Adult'][label]
            adult = subset[subset['Age Group'] == 'Adult'][label]
        
            if len(young) >= 10 and len(adult) >= 10:
                _, p_val = ttest_ind(young, adult, equal_var=False)
                results.append({
                    'Test': 'T-test',
                    'Group': f'Gender: {gender}',
                    'Comparison': 'Young Adult vs Adult ({label})',
                    'p-value': round(p_val, 4),
                    'Significant': p_val < 0.05
                })
                print(f"\n{gender} | {label} ({len(subset)} total samples)")
                print(f"   Young Adult : n={len(young)}, Mean = {young.mean():.2f}")
                print(f"   Adult       : n={len(adult)}, Mean = {adult.mean():.2f}")
                print(f"   p-value     : {p_val:.4f} {'→ Significant difference' if \
                  p_val < 0.05 else '→ No significant difference'}")
                
            else: print(f"   Skipped {label} - insufficient samples")
            
    # T-tests by Gender within each Age Group
    print('\n--------- T-tests by gender within each age group ---------')
    for age_group in sorted(df['Age Group'].unique()):
        subset = df[df['Age Group'] == age_group]
        
        for label in numerical_cols:
            male = subset[subset['Gender'] == 'Male'][label]
            female = subset[subset['Gender'] == 'Female'][label]
            
            if len(male) >= 10 and len(female) >= 10:
                _, p_val = ttest_ind(male, female, equal_var=False)
                results.append({
                    'Test': 'T-test',
                    'Group': f'Age Group: {age_group}',
                    'Comparison': f'Male vs Female ({label})',
                    'p-value': round(p_val, 4),
                    'Significant': p_val < 0.05
                })
                print(f"\n{age_group} | {label}")
                print(f"   Male  : n={len(male)}, mean={male.mean():.2f}")
                print(f"   Female: n={len(female)}, mean={female.mean():.2f}")
                print(f"   p-value: {p_val:.4f} → {'Significant' if p_val < 0.05 else 'Not significant'}")
        
    return

def find_correlations(df):
    # Generate correlation matrix (default: Pearson)
    corr_matrix = df.corr(numeric_only=True)

    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='RdBu')
    plt.show()
    
    return

