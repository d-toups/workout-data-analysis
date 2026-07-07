'''
Author: Dennis Toups
Date: 3 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

from utils import convert_cat_num

################### Function Definition #######################################

""" Engineer Features *********************************************************
Purpose: Normalize and prepare appropriate features for analysis

Inputs: workout dataframe 
    
Outputs: Updated df with new features Calories Per Minute, Age Group, and Body 
Fat Group. Modified Experience Level values to align with analysis tools.

----------------------------------------------------------------------------"""

def engineer_features(df):
    # Add calories per minute feature
    df['Calories Per Minute'] = df['Calories Burned'] / df[\
                                                    'Session Duration (minutes)']
    # Create Age Group bins
    df['Age Group'] = pd.cut(df['Age'], 
                             bins=[17, 34, 64], 
                             labels=['Young Adult', 'Adult'])
    
    # Remove any rows that were not binned (including 'nan')
    df = df[df['Age Group'].notna()].copy()
    
    # Convert to string
    df['Age Group'] = df['Age Group'].astype(str)
    
    # Create Body Fat Percentage Bins
    bins_dict = {
    'Male': [0, 13, 17, 24, 100],
    'Female': [0, 20, 24, 31, 100]
    }

    labels = ['Athlete', 'Fit', 'Average', 'Obese']

    df['Body Fat Group'] = pd.NA
    
    for gender, bin_edges in bins_dict.items():
        mask = df['Gender'] == gender
        df.loc[mask, 'Body Fat Group'] = pd.cut(
            df.loc[mask, 'Fat Percentage'],
            bins=bin_edges,
            labels=labels,
            right=True,
            include_lowest=True
            )
    
    # Remove any rows that were not binned (including 'nan')
    df = df[df['Body Fat Group'].notna()].copy()
    
    # Ensure Experience Level starts at 0
    if df['Experience Level'].min() != 0:
        df['Experience Level'] = df['Experience Level'] - df['Experience Level'].min()
    
    # Convert categorical to numerical
    cols = ['Workout Type', 'Body Fat Group', 'Age Group', 'Gender']
    convert_cat_num(df, cols)
    
    return df

