'''
Author: Dennis Toups
Date: 3 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
from sklearn.preprocessing import LabelEncoder

################### Function Definition #######################################

""" Convert Categorical to Numerical ******************************************
Purpose: Take object dtype targets, make them numeric

Inputs: df - dataset consisting workout metrics
        cols - target labels for which to convert classes to numeric
    
Outputs: Converts df in place, prints mapping
----------------------------------------------------------------------------"""

def convert_cat_num(df, cols):
    for col in cols:
        # Convert categorical to numerical
        le_col = LabelEncoder()
    
        # Convert, ensure each starts at 0
        df[f"{col} Encoded"] = le_col.fit_transform(df[col])
        if df[f"{col} Encoded"].min() != 0:
            df[f"{col} Encoded"] = df[col] - df[col].min()
        
        # Show the mapping
        #mapping = dict(zip(le_col.classes_, le_col.transform(le_col.classes_)))
        #print(f"{col} Mapping:")
        #for item, code in sorted(mapping.items()):
        #    print(f"  {code} → {item}")
    
    return

