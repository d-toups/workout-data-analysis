'''
Author: Dennis Toups
Date: 7 July 2026
'''

from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split   
import seaborn as sns
import matplotlib.pyplot as plt

""" Tune & Evaluate, Final Evaluation *****************************************
Purpose: Having identified the top performing models and features for each 
target, now the models' hyperparameters are tuned for maximum accuracy and 
given final performance evaluation.

Inputs: Workout dataframe, individual model performance results.
    
Outputs: Dictionary containing the best model information for each target.

----------------------------------------------------------------------------"""

def tune_and_evaluate(df, top_features_dict, random_state=42):
    results_dict = top_features_dict
    for target_col, config in top_features_dict.items():
        X = df[config['features']]
        y = df[target_col]
        
        if config['model'] == 'XGBoost':
            model = XGBClassifier(random_state=random_state, eval_metric='mlogloss', 
                                  tree_method='hist', device='cuda')
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.05, 0.1],
                'subsample': [0.8, 1.0]
                }
        elif config['model'] == 'Random Forest':
            model = RandomForestClassifier(random_state=random_state, n_jobs=-1)
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5]
            }
    
        cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)
        
        grid_search = GridSearchCV(
            model, param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=0
        )
        
        grid_search.fit(X, y)
        
        print(f"\nBest parameters for {target_col}: {grid_search.best_params_}")
        print(f"{target_col} Best CV Accuracy: {grid_search.best_score_:.4f}")
        
        results_dict[target_col]['best_estimator'] = grid_search.best_estimator_
        results_dict[target_col]['best_parameters'] = grid_search.best_params_
        results_dict[target_col]['best_score'] = grid_search.best_score_
        
    return results_dict

def final_evaluation(df, results_dict, random_state=42):
    best_models = {}
    for target_col, config in results_dict.items():
        X = df[config['features']]
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=random_state, stratify=y
            )
        best_model = config['best_estimator']
        
        # Final fit on train set
        best_model.fit(X_train, y_train)
        y_pred = best_model.predict(X_test)
        
        best_models[target_col] = best_model
        
        print(f"\nFinal Evaluation - {target_col}")
        print("="*50)
        print(classification_report(y_test, y_pred))
        
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {target_col}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()
    
    return best_models
