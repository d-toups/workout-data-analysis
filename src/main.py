'''
Author: Dennis Toups
Date: 7 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
from data_loader import load_dataset, clean_dataset
from feature_engineering import engineer_features
from eda import (
    plot_workout_by_age_group,
    plot_cpm,
    stats,
    find_correlations
    )
from feature_selection import (
    feature_importance,
    run_random_forest,
    run_xgboost,
    run_knn,
    select_models_features,
    print_models
    )
from modeling import tune_and_evaluate, final_evaluation

import warnings
warnings.filterwarnings('ignore')

################### Execution #################################################
if __name__ == "__main__":
    ## Load and Clean the Dataset
    df_raw = load_dataset("gym_members_exercise_tracking.csv")
    df_clean = clean_dataset(df_raw)

    ## Feature engineering
    df = engineer_features(df_clean)

    ## EDA
    # 1. Plot Workout Preference by Age Group and Gender
    plot_workout_by_age_group(df)
    
    # 2. Plot Calories per Minute by Workout Type and Gender
    plot_cpm(df)
    
    # 3. Conduct chi-square and t-testing on dataset
    stats(df)
    
    # 4. Look for correlations among data
    find_correlations(df)
    
    ## Feature Selection
    rf_top_features_dict, xgb_top_features_dict, knn_top_features_dict = feature_importance(df)
    rf_result = xgb_result = knn_result = {}
    
    # 1. Random Forest Model
    rf_result = run_random_forest(df, rf_top_features_dict)
    
    # 2. XGBoost Model
    xgb_result = run_xgboost(df, xgb_top_features_dict)
    
    # 3. kNN
    knn_result = run_knn(df, xgb_top_features_dict)
    
    # 4. Select model, features with highest accuracy
    best_features_models = select_models_features(df, rf_result, xgb_result, knn_result)
    
    print_models(best_features_models)
    
    ## Modeling
    results_dict = tune_and_evaluate(df, best_features_models)
    
    final_evaluation(df, results_dict)