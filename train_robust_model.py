"""
ROBUST ML MODEL WITH BALANCED DATA USING SMOTE
This creates a truly balanced dataset for better ML performance
"""
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from core.dataset import DatasetLoader
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib

print("=" * 80)
print("🚀 TRAINING ROBUST ML MODEL WITH BALANCED DATA (SMOTE)")
print("=" * 80)

data_path = 'data'
model_path = 'models'
os.makedirs(model_path, exist_ok=True)

# ========== 1. LOAD DATA ==========
print("\n📂 STEP 1: Loading NASA Promise Dataset...")
loader = DatasetLoader(data_path)
df = loader.load_all_data()
df = loader.clean_data(df)
print(f"   ✅ Loaded {len(df)} samples")

# ========== 2. FEATURE SELECTION ==========
print("\n📊 STEP 2: Feature Selection & Engineering...")
feature_cols = ['loc', 'v(g)', 'n', 'lOCode', 'branchCount', 'uniq_Op', 'uniq_Opnd']
existing = [f for f in feature_cols if f in df.columns]

X = df[existing].copy()
y = df.iloc[:, -1]

# Handle target
if y.dtype == 'object' or y.dtype == 'bool':
    y = y.astype(str).map({'true': 1, 'false': 0, 'True': 1, 'False': 0})
else:
    y = pd.to_numeric(y, errors='coerce')
    y = (y > 0).astype(int)
y = y.fillna(0)

# Convert to numeric
for col in X.columns:
    X[col] = pd.to_numeric(X[col], errors='coerce')
X = X.fillna(X.mean())

# Feature engineering
X['complexity_per_loc'] = X['v(g)'] / (X['loc'] + 1)
if 'uniq_Op' in X.columns:
    X['operators_per_loc'] = X['uniq_Op'] / (X['loc'] + 1)

print(f"   ✅ Features: {list(X.columns)}")
print(f"   ✅ Original distribution: No Defect={( y==0).sum()}, Defect={(y==1).sum()}")
print(f"   ⚖️ Imbalance ratio: {(y==0).sum() / (y==1).sum():.2f}:1")

# ========== 3. SPLIT DATA ==========
print("\n📂 STEP 3: Train/Val/Test Split (70/15/15)...")
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

print(f"   Train: {len(X_train)} samples (No Defect={( y_train==0).sum()}, Defect={(y_train==1).sum()})")
print(f"   Val: {len(X_val)} samples")
print(f"   Test: {len(X_test)} samples")

# ========== 4. TRAIN WITH SMOTE ==========
print("\n🤖 STEP 4: Training Random Forest with SMOTE Balancing...")
print("   SMOTE will create synthetic samples of minority class (Defect)")

pipeline = ImbPipeline([
    ('scaler', StandardScaler()),
    ('smote', SMOTE(random_state=42, k_neighbors=5)),
    ('classifier', RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=15,
        min_samples_leaf=8,
        random_state=42,
        n_jobs=-1
    ))
])

pipeline.fit(X_train, y_train)
print("   ✅ Model trained successfully!")

# Check balanced data after SMOTE
smote = pipeline.named_steps['smote']
X_train_resampled, y_train_resampled = smote.fit_resample(
    pipeline.named_steps['scaler'].fit_transform(X_train), 
    y_train
)
print(f"   📊 After SMOTE: No Defect={( y_train_resampled==0).sum()}, Defect={(y_train_resampled==1).sum()}")
print(f"   ✅ Data is now BALANCED!")

# ========== 5. EVALUATION ==========
print("\n📈 STEP 5: Model Evaluation...")

# Training
train_pred = pipeline.predict(X_train)
train_acc = accuracy_score(y_train, train_pred)
print(f"\n   Training Accuracy: {train_acc:.4f}")

# Validation
val_pred = pipeline.predict(X_val)
val_proba = pipeline.predict_proba(X_val)[:, 1]
val_acc = accuracy_score(y_val, val_pred)
val_auc = roc_auc_score(y_val, val_proba)
print(f"   Validation Accuracy: {val_acc:.4f}")
print(f"   Validation AUC-ROC: {val_auc:.4f}")

# Test
test_pred = pipeline.predict(X_test)
test_proba = pipeline.predict_proba(X_test)[:, 1]
test_acc = accuracy_score(y_test, test_pred)
test_auc = roc_auc_score(y_test, test_proba)

print(f"\n   🧪 TEST SET RESULTS:")
print(f"   Accuracy: {test_acc:.4f}")
print(f"   AUC-ROC: {test_auc:.4f}")

# Overfitting check
if train_acc - val_acc > 0.15:
    print(f"\n   ⚠️ WARNING: Possible overfitting (diff: {train_acc - val_acc:.4f})")
else:
    print(f"\n   ✅ No significant overfitting detected")

# Classification report
print(f"\n   📋 Classification Report:")
print(classification_report(y_test, test_pred, target_names=['No Defect', 'Defect']))

# Confusion matrix
print(f"\n   🔢 Confusion Matrix:")
cm = confusion_matrix(y_test, test_pred)
print(f"      True Negatives: {cm[0][0]}, False Positives: {cm[0][1]}")
print(f"      False Negatives: {cm[1][0]}, True Positives: {cm[1][1]}")

# Feature importance
rf_model = pipeline.named_steps['classifier']
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n   🔝 Top 5 Feature Importances:")
for idx, row in importances.head(5).iterrows():
    print(f"      {row['feature']}: {row['importance']:.4f}")

# ========== 6. SAVE MODEL ==========
print("\n💾 STEP 6: Saving Model...")
joblib.dump(pipeline, os.path.join(model_path, 'model.pkl'))
joblib.dump(list(X.columns), os.path.join(model_path, 'feature_names.pkl'))
joblib.dump(X.mean().to_dict(), os.path.join(model_path, 'feature_means.pkl'))

print(f"   ✅ Model saved to: {model_path}/model.pkl")
print(f"   ✅ Features saved: {list(X.columns)}")

print("\n" + "=" * 80)
print("✅ ROBUST ML MODEL TRAINING COMPLETE!")
print("   The model is now trained on BALANCED data using SMOTE")
print("   It should give much better predictions for both classes!")
print("=" * 80)
