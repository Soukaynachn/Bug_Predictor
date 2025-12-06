from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class ModelTrainer:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        return accuracy, report

    def save_model(self, filename='model.pkl'):
        path = os.path.join(self.model_path, filename)
        joblib.dump(self.model, path)
        return path

    def load_model(self, filename='model.pkl'):
        path = os.path.join(self.model_path, filename)
        if os.path.exists(path):
            self.model = joblib.load(path)
        else:
            raise FileNotFoundError("Model file not found")
