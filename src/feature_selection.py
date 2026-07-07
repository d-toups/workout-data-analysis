'''
Author: Dennis Toups
Date: 7 July 2026
'''

################### Imports and Setup #########################################
# Import librabries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.inspection import permutation_importance

from sklearn.model_selection import (
    StratifiedKFold, 
    cross_val_score,
    train_test_split,
    GridSearchCV
    )

from xgboost import XGBClassifier
import warnings; warnings.filterwarnings('ignore')

# Standardize plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

RANDOM_STATE = 42
TEST_SIZE = 0.2
NEIGHBORS = 4

################### Function Definition #######################################

""" Feature Selection *********************************************************
Purpose: Identify top features to predict desired targets.

Inputs: Workout dataframe

Outputs: Dictionaries containing top feature information per target per 
modeling method (Random Forest, XGBoost, kNN).

----------------------------------------------------------------------------"""

def feature_importance(df, random_state=RANDOM_STATE, top_n=10):
    
    X_cols_master = [
        'Age',
        'Gender Encoded', 
        'Session Duration (minutes)',
        'Workout Type Encoded', 
        'Fat Percentage', 
        'Experience Level',
        'Body Fat Group Encoded', 
        'Calories Per Minute'
        ]
    # Note: Because Session Duration is highly correlated with Workout Frequency, 
    # only Session Duration chosen to avoid redundancy. For same reason, CPM is
    # chosen over Calories Burned and Average BPM. Similarly, Age chosen over 
    # Age Group Encoded as Age consistently achieves higher feature importance.
    
    target_cols = [ 
        'Body Fat Group Encoded', 
        'Experience Level', 
        'Age Group Encoded'
        ]
    
    rf_top_features_dict = {} 
    xgb_top_features_dict = {}
    knn_top_features_dict = {}
    importance_results = {}

    for target_col in target_cols:
        X_cols = X_cols_master
        
        if df[target_col].nunique() < 2:
            continue
        
        # Prevent leakage (applicable to both RF and XGB)
        X_cols = [col for col in X_cols if col != target_col]
        if 'body fat' in target_col.lower():
            X_cols = [col for col in X_cols if 'fat percentage' not in col.lower()]
        if 'age group' in target_col.lower():
            X_cols.remove('Age')
        
        X = df[X_cols]
        y = df[target_col]
        
        #------------- Random Forest
        rf = RandomForestClassifier(random_state=random_state, n_jobs=-1)
        rf.fit(X, y)
        
        # Get feature importance
        rf_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': rf.feature_importances_,
            'model': 'Random Forest'
        }).sort_values('importance', ascending=False)
        
        # Get top features
        rf_top_features = rf_importance[rf_importance['importance'] > 0.1]['feature'].tolist()
        rf_top_features_dict[target_col] = {
            'features': rf_top_features
            }
        
        #------------- XGBoost
        xgb = XGBClassifier(random_state=RANDOM_STATE, eval_metric='mlogloss')
        xgb.fit(X, y)
        
        xgb_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': xgb.feature_importances_,
            'model': 'XGBoost'
        }).sort_values('importance', ascending=False)
        
        # Get top features
        if target_col == 'Age Group Encoded':
            xgb_top_features = xgb_importance[xgb_importance['importance'] > 0.12]['feature'].tolist()
        else:
            xgb_top_features = xgb_importance[xgb_importance['importance'] > 0.09]['feature'].tolist()
            
        xgb_top_features_dict[target_col] = {
            'features': xgb_top_features
            }
        
        #------------- kNN
        # Scale features (kNN is distance-based)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        knn = KNeighborsClassifier(n_neighbors=NEIGHBORS)
        knn.fit(X_scaled, y)
        
        result = permutation_importance(knn, X_scaled, y, n_repeats=10, 
                                        random_state=RANDOM_STATE, n_jobs=-1)

        knn_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': result.importances_mean,
            'model': 'KNN'
            }).sort_values('importance', ascending=False)
        
        # Get top features
        knn_top_features = knn_importance[knn_importance['importance'] > 0.1]['feature'].to_list()
        knn_top_features_dict[target_col] = {
            'features': knn_top_features
            }
        
        # Combine and store
        combined = pd.concat([rf_importance, xgb_importance, knn_importance])
        importance_results[target_col] = combined
        
        #if __name__ == "__main__":
        # Plot RF, XGB, KNN importance results side-by-side
        plt.figure(figsize=(12, 6))
        sns.barplot(data=combined, x='importance', y='feature', hue='model')
        plt.title(f'Feature Importance Comparison - Predicting: {target_col}')
        plt.tight_layout()
        plt.show()
        
    return rf_top_features_dict, xgb_top_features_dict, knn_top_features_dict

""" Initial Modeling Functions ************************************************
Purpose: Implement and assess Random Forest, XGBoost, and kNN models' ability
to predict workout type preference, body fat group, experience level, and 
age group.

Inputs: Workout dataframe top features
    
Outputs: Plots, classification reports assessing model performance as well as a 
dictionary containing results for each model.

----------------------------------------------------------------------------"""

def run_random_forest(df, feature_dict, random_state=RANDOM_STATE):
    rf_result = {}
    for target_col, top_features in feature_dict.items():
        
        X = df[top_features['features']]
        y = df[target_col]
    
        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
            )
        
        # Final Model
        rf_final = RandomForestClassifier(
            n_estimators=90,
            max_depth=8,
            random_state=RANDOM_STATE,
            n_jobs=-1
            )
        
        rf_final.fit(X_train, y_train)
        
        # Cross-Validation Score
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
        cv_scores = cross_val_score(rf_final, X_train, y_train, cv=cv, 
                                    scoring='accuracy')
        
        
        print(f"RF {target_col} CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        
        # Test Set Evaluation
        y_pred = rf_final.predict(X_test)
        
        print(f"\n{target_col} Classification Report:")
        print(classification_report(y_test, y_pred))
        """
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
        plt.title(f"Confusion Matrix - {target_col} (Random Forest)")
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()
        
        # Feature Importance Plot
        importance = pd.DataFrame({
            'feature': top_features['features'],
            'importance': rf_final.feature_importances_
            }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=importance, palette='viridis')
        plt.title(f"Feature Importance - {target_col} (Random Forest)")
        plt.show()
        """
        rf_result[target_col] = {
            'model': 'rf',
            'score': cv_scores.mean(),
            'features': top_features['features']
            }
            
    return rf_result

def run_xgboost(df, feature_dict, random_state=RANDOM_STATE):
    xgb_result = {}
    
    for target_col, top_features in feature_dict.items():
        X = df[top_features['features']]
        y = df[target_col]
        
        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=random_state, stratify=y
            )
        
        # XGBoost with hyperparameter tuning
        xgb = XGBClassifier(random_state=random_state, eval_metric='mlogloss')
        
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8, 1.0]
            }
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        
        grid_search = GridSearchCV(
            xgb, param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=1
            )
        
        grid_search.fit(X_train, y_train)
        
        #print(f"XGB {target_col} Best parameters: {grid_search.best_params_}")
        print(f"XGB {target_col} Best CV Accuracy: {grid_search.best_score_:.4f}")
        
        # Final evaluation
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        """
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {target_col} Prediction (XGBoost)')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()
        
        # Feature Importance Plot
        importance = pd.DataFrame({
            'feature': X.columns,
            'importance': best_model.feature_importances_
            }).sort_values('importance', ascending=False)
         
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=importance, palette='viridis')
        plt.title(f'Feature Importance - Predicting {target_col} (XGBoost)')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.show()
        """
        xgb_result[target_col] = {
            'model': 'xgb',
            'score': grid_search.best_score_,
            'features': top_features['features']
            }
        
    return xgb_result

def run_knn(df, feature_dict, random_state = RANDOM_STATE):
    knn_result = {}
    
    for target_col, top_features in feature_dict.items():
        X = df[top_features['features']]
        y = df[target_col]
    
        # Scale features (KNN is distance-based)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=TEST_SIZE, random_state=random_state, stratify=y
            )   
        
        # kNN
        knn = KNeighborsClassifier(n_neighbors=NEIGHBORS)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        
        # Cross-Validation Score
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
        cv_scores = cross_val_score(knn, X_scaled, y, cv=cv, 
                                    scoring='accuracy', n_jobs=-1)
        
        print(f"kNN {target_col} {NEIGHBORS} neighbors CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"KNN {target_col} Classification Report:")
        print(classification_report(y_test, y_pred))
        """
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix - Workout Type Prediction (kNN)')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()
        """
        knn_result[target_col] = {
            'model': 'knn',
            'score': cv_scores.mean(),
            'features': top_features['features']
            }
    
    return knn_result

""" Model & Feature Selection and Results Output ******************************
Purpose: Compare performance for each target and select & display results for 
the best model and features.

Inputs: Workout dataframe, individual model performance results.
    
Outputs: Dictionary containing the best model information for each target.

----------------------------------------------------------------------------"""

def select_models_features(df, rf_result, xgb_result, knn_result):
    best_models = {}
    result = {
        'Random Forest': rf_result,
        'XGBoost': xgb_result,
        'KNN': knn_result
    }
    
    target_cols = list(rf_result.keys())
    
    for target_col in target_cols:
        best_score = -1
        best_model_name = None
        best_config = None

        for model_name, result_dict in result.items():
            if target_col in result_dict:
                config = result_dict[target_col]
                if config['score'] > best_score:
                    best_score = config['score']
                    best_model_name = model_name
                    best_config = config
        
        best_models[target_col] = {
            'features': best_config['features'],
            'model': best_model_name,
            'best_estimator': None,
            'best_parameters': None,
            'best_score': best_score
        }
    
    return best_models

def print_models(config_dict):
    for target, config in config_dict.items():
        print(
            f"{target}: {config['best_score']:.4f} accuracy using {config['model']} and features {config['features']}\n"
        )
    return