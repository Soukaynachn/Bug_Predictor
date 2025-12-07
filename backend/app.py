from flask import Flask, render_template, request, jsonify
import os

from core.dataset import DatasetLoader
from core.model import ModelTrainer
from core.features import FeatureExtractor

app = Flask(__name__)

# Configuration
app.config['DATA_FOLDER'] = os.path.join(os.getcwd(), 'data')
app.config['MODEL_FOLDER'] = os.path.join(os.getcwd(), 'models')

# Ensure directories exist
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)

# Initialize components
dataset_loader = DatasetLoader(app.config['DATA_FOLDER'])
model_trainer = ModelTrainer(app.config['MODEL_FOLDER'])
feature_extractor = FeatureExtractor()

# Load model and feature names at startup
print("🚀 Loading trained model...")
try:
    model_trainer.load_model()
    
    import joblib
    feature_names_path = os.path.join(app.config['MODEL_FOLDER'], 'feature_names.pkl')
    feature_means_path = os.path.join(app.config['MODEL_FOLDER'], 'feature_means.pkl')
    
    if os.path.exists(feature_names_path):
        TRAINED_FEATURE_NAMES = joblib.load(feature_names_path)
        print(f"✅ Model loaded successfully with {len(TRAINED_FEATURE_NAMES)} features")
        
        # Load feature means for missing values
        if os.path.exists(feature_means_path):
            FEATURE_MEANS = joblib.load(feature_means_path)
            print(f"✅ Feature means loaded")
        else:
            FEATURE_MEANS = {}
            print("⚠️ Feature means not found, using zeros")
        
        # Check model file timestamp
        model_path = os.path.join(app.config['MODEL_FOLDER'], 'model.pkl')
        if os.path.exists(model_path):
            import time
            mod_time = os.path.getmtime(model_path)
            mod_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
            print(f"📅 Model last updated: {mod_time_str}")
    else:
        TRAINED_FEATURE_NAMES = None
        FEATURE_MEANS = {}
        print("⚠️ Feature names not found. Using fallback prediction.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    TRAINED_FEATURE_NAMES = None
    FEATURE_MEANS = {}

@app.route('/')
def index():
    return render_template('index.html')

# Allowed extensions configuration
ALLOWED_EXTENSIONS = {'py', 'java', 'cpp', 'c', 'h', 'js', 'php', 'ts', 'cs', 'go', 'rb'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Handle Text Paste
    if 'code_text' in request.form:
        code = request.form['code_text']
        if not code or not code.strip():
             return jsonify({'error': 'Please provide some code to analyze.'}), 400
        
        # Heuristic 1: Length check
        if len(code.strip()) < 10:
             return jsonify({'error': 'The provided text is too short to be valid code.'}), 400

        # Heuristic 2: Hybrid Syntax Check
        # Try to parse as Python
        import ast
        is_python = False
        try:
            tree = ast.parse(code)
            is_python = True
            
            # Anti-Garbage Check: Reject trivial expressions (e.g. single word "asdf")
            if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
                expr = tree.body[0].value
                # If it's just a single Name (variable) or Constant (string/num) -> Garbage
                if isinstance(expr, (ast.Name, ast.Constant)):
                    is_python = False
                    
        except SyntaxError:
            is_python = False
        
        # If not Python, check for common code symbols (C++, Java, JS, etc.)
        # Real code usually contains at least one of these: { } ; ( ) =
        symbols = ['{', '}', ';', '(', ')', '=']
        has_symbols = any(char in code for char in symbols)

        if not is_python and not has_symbols:
            # It's not Python and lacks structure -> Garbage
            return jsonify({'error': 'No valid code structure detected (missing syntax like { } ; =).'}), 400

        features = feature_extractor.extract_from_code(code, "pasted_code.py")
        return predict_and_render(features, "Pasted Code")

    # 2. Handle File Upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1] if '.' in file.filename else 'no extension'
        return jsonify({'error': f'Unsupported file type: .{ext}. Please upload a code file.'}), 400

    # 3. Handle File Analysis
    try:
        content = file.read().decode('utf-8', errors='ignore')

        if not content.strip():
             return jsonify({'error': 'The file is empty. Please upload a file with code.'}), 400

        features = feature_extractor.extract_from_code(content, file.filename)
        return predict_and_render(features, file.filename)
                             
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def predict_and_render(features, filename):
    if not features:
        return jsonify({'error': 'Failed to extract features'}), 400
    
    # Strict Validation: Ensure code has actual substance
    # Radon/Lizard return 0 LOC/SLOC for plain text or comments-only files
    if features.get('loc', 0) == 0 and features.get('sloc', 0) == 0:
         return jsonify({'error': 'No valid code structure detected. Please check your input.'}), 400
    
    import pandas as pd
    
    try:
        # Use pre-loaded model and feature names
        if TRAINED_FEATURE_NAMES and model_trainer.model:
            # Create a feature vector matching the model's expected input
            feature_vector = {}
            
            # Map basic features
            for feat_name in TRAINED_FEATURE_NAMES:
                if feat_name == 'loc' and 'loc' in features:
                    feature_vector[feat_name] = features['loc']
                elif feat_name == 'v(g)' and 'cyclomatic_complexity' in features:
                    feature_vector[feat_name] = features['cyclomatic_complexity']
                elif feat_name == 'n' and 'halstead_volume' in features:
                    feature_vector[feat_name] = features['halstead_volume']
                elif feat_name == 'lOCode' and 'sloc' in features:
                    feature_vector[feat_name] = features['sloc']
                elif feat_name == 'complexity_per_loc':
                    # Engineered feature
                    loc_val = features.get('loc', 1)
                    complexity_val = features.get('cyclomatic_complexity', 0)
                    feature_vector[feat_name] = complexity_val / (loc_val + 1)
                elif feat_name == 'operators_per_loc':
                    # Engineered feature (approximate with 0 since we don't extract this)
                    feature_vector[feat_name] = FEATURE_MEANS.get(feat_name, 0)
                else:
                    # Use mean for features we can't extract
                    feature_vector[feat_name] = FEATURE_MEANS.get(feat_name, 0)
            
            # Create DataFrame with correct column order
            X_pred = pd.DataFrame([feature_vector], columns=TRAINED_FEATURE_NAMES)
            
            # Get prediction probability from ML model
            risk_proba = model_trainer.model.predict_proba(X_pred)[0]
            ml_score = risk_proba[1]  # Probability of defect (class 1)
            
            # Calculate heuristic score based on code metrics
            heuristic_score = 0.0
            loc_val = features.get('loc', 0)
            complexity_val = features.get('cyclomatic_complexity', 0)
            halstead_val = features.get('halstead_volume', 0)
            
            # Heuristic rules
            if loc_val > 150: heuristic_score += 0.25
            elif loc_val > 100: heuristic_score += 0.15
            
            if complexity_val > 10: heuristic_score += 0.35
            elif complexity_val > 5: heuristic_score += 0.20
            elif complexity_val > 3: heuristic_score += 0.10
            
            if halstead_val > 500: heuristic_score += 0.15
            elif halstead_val > 300: heuristic_score += 0.08
            
            heuristic_score = min(1.0, heuristic_score)
            
            # Hybrid approach: blend ML and heuristic
            # If ML gives very low score but metrics suggest risk, boost it
            if ml_score < 0.1 and heuristic_score > 0.3:
                # ML is too conservative, use more heuristic
                risk_score = 0.3 * ml_score + 0.7 * heuristic_score
            else:
                # ML seems reasonable, use it more
                risk_score = 0.7 * ml_score + 0.3 * heuristic_score
            
        else:
            # Fallback if model not loaded
            risk_score = 0.5
            
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to heuristic-based prediction
        complexity = features.get('cyclomatic_complexity', 1)
        loc = features.get('loc', 0)
        risk_score = min(1.0, (complexity / 10.0) * 0.5 + (loc / 100.0) * 0.5)

    return render_template('result.html', 
                            filename=filename, 
                            risk_score=risk_score, 
                            metrics=features)

import tempfile
import shutil
import uuid
import git

@app.route('/analyze_repo', methods=['POST'])
def analyze_repo():
    repo_url = request.form.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'Please provide a Git Repository URL.'}), 400
    
    # Create temp directory
    temp_dir = os.path.join(tempfile.gettempdir(), f'repo_{uuid.uuid4()}')
    
    results = []
    
    try:
        # Clone repo
        print(f"Cloning {repo_url} into {temp_dir}...")
        git.Repo.clone_from(repo_url, temp_dir, depth=1)
        
        # Iterate files
        for root, dirs, files in os.walk(temp_dir):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                if allowed_file(file):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, temp_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Validate content (similar to single file)
                        if not content.strip() or (len(content.strip()) < 10):
                            continue # Skip empty/dummy files
                            
                        # Basic heuristics checks (optional here, or assume repo code is somewhat valid)
                         
                        features = feature_extractor.extract_from_code(content, file)
                        
                        if not features or (features.get('loc', 0) == 0):
                            continue

                        # Reuse prediction logic (refactor if strictly needed, but duplicating small block is safer for now to avoid breaking existing flow)
                        import pandas as pd
                         # ... Use strict logic ...
                        risk_score = 0.5 # default
                        
                        # --- Prediction Logic Start (Condensed) ---
                        if TRAINED_FEATURE_NAMES and model_trainer.model:
                            feature_vector = {}
                            for feat_name in TRAINED_FEATURE_NAMES:
                                if feat_name == 'loc': feature_vector[feat_name] = features.get('loc', 0)
                                elif feat_name == 'v(g)': feature_vector[feat_name] = features.get('cyclomatic_complexity', 0)
                                elif feat_name == 'n': feature_vector[feat_name] = features.get('halstead_volume', 0)
                                elif feat_name == 'lOCode': feature_vector[feat_name] = features.get('sloc', 0)
                                elif feat_name == 'complexity_per_loc':
                                     feature_vector[feat_name] = features.get('cyclomatic_complexity', 0) / (features.get('loc', 1) + 1)
                                else:
                                     feature_vector[feat_name] = FEATURE_MEANS.get(feat_name, 0)
                            
                            X_pred = pd.DataFrame([feature_vector], columns=TRAINED_FEATURE_NAMES)
                            ml_score = model_trainer.model.predict_proba(X_pred)[0][1]
                            
                            # Simple heuristic boost
                            heuristic_score = 0
                            if features.get('loc',0) > 100: heuristic_score += 0.2
                            if features.get('cyclomatic_complexity',0) > 5: heuristic_score += 0.3
                            heuristic_score = min(1.0, heuristic_score)

                            risk_score = 0.7 * ml_score + 0.3 * heuristic_score
                        # --- Prediction Logic End ---
                        
                        results.append({
                            'filename': rel_path,
                            'risk_score': round(risk_score, 4),
                            'metrics': features,
                            'risk_label': 'High' if risk_score > 0.5 else 'Low'
                        })
                        
                    except Exception as e:
                        print(f"Skipping file {rel_path}: {e}")
                        continue

    except Exception as e:
        return jsonify({'error': f'Failed to analyze repository: {str(e)}'}), 500
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass 
    
    # Sort by risk descending
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    
    return render_template('repo_result.html', 
                          repo_url=repo_url,
                          results=results,
                          file_count=len(results))

if __name__ == '__main__':
    app.run(debug=True)
