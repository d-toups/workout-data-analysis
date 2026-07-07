'''
Author: Dennis Toups
Date: 3 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
import pandas as pd
import warnings; warnings.filterwarnings('ignore')

################### Function Definition #######################################

""" Load Dataset **************************************************************
Purpose: Reads .csv dataset into pandas dataframe

Inputs: filepath - file to be read in
    
Outputs: df - dataset in dataframe format

----------------------------------------------------------------------------"""

def load_dataset(filepath):
    # Use specified columns to read in Age, Gender, Workout Type, Workout
    # Duration, and Calories Burned
    df = pd.read_csv(filepath, usecols=[0, 1, 5, 7, 8, 9, 10, 12, 13])
    return df

""" Clean Dataset *************************************************************
Purpose: Clean raw dataset, create Calories Per Minute feature

Inputs: df - dataset consisting workout metrics
    
Outputs: df - cleaned dataset to be analyzed

----------------------------------------------------------------------------"""

def clean_dataset(df):
    # Remove any rows with non-numerical values for numerical features
    numerical_cols = df.select_dtypes(include='number').columns.tolist()
    
    for col in numerical_cols:
        df = df[pd.to_numeric(df[col], errors='coerce').notna()] 
        
    # Clean strings to title format
    df.columns = [col.title().replace("_", " ") for col in df.columns]
    df['Gender'] = df.Gender.str.title()
    
    # We want to keep the HIIT elements uppercase, all others title case
    df['Workout Type'] = df['Workout Type'].apply( lambda x: x.upper() if
                                                  str(x).isupper() else
                                                  x.title())
    
    # Transform Session Duration from hours to minutes, rename
    df['Session Duration (minutes)'] = 60 * df['Session Duration (Hours)']
        
    # Remove Session Duration (Hours) column
    df.drop('Session Duration (Hours)', axis=1, inplace=True)
    
    # Filter out invalid values for gender
    df = df[df['Gender'].isin(['Male', 'Female'])]
    
    df = df.dropna().copy()  # Drop any real missing values
        
    #print(f"\nFinal dataset shape after cleaning: {df.shape}")
    
    return df