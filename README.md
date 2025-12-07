# 🐛 Bug Predictor PRO

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Advanced AI-powered software defect prediction** - Identify risk-prone code before it becomes a problem

Bug Predictor is an intelligent web application that leverages Machine Learning and static code analysis to predict defect-prone areas in your software projects. Built with Random Forest algorithms and trained on the NASA Promise dataset, it provides actionable insights to help development teams focus their testing and code review efforts where they matter most.

---

## 📋 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Supported Languages](#-supported-languages)
- [Technical Details](#-technical-details)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 **Three Analysis Modes**
- **📁 Upload File** - Analyze individual source code files
- **📝 Paste Code** - Quick analysis of code snippets
- **🔗 Git Repository** - Comprehensive analysis of entire repositories

### 🧠 **AI-Powered Predictions**
- Random Forest ML model trained on NASA Promise datasets
- SMOTE algorithm for balanced class prediction
- Hybrid scoring combining ML predictions with code complexity heuristics

### 📊 **Comprehensive Metrics**
- Cyclomatic Complexity
- Lines of Code (LOC)
- Halstead Metrics
- Maintainability Index
- Risk assessment and recommendations

### 🎨 **User-Friendly Interface**
- Clean, modern web interface
- Real-time analysis results
- Detailed reports with actionable insights

---

## 🔍 How It Works

Bug Predictor analyzes your code through three stages:

1. **Code Parsing** - Extracts structure and complexity metrics
2. **ML Prediction** - Random Forest model evaluates defect probability
3. **Risk Scoring** - Combines ML output with heuristic analysis for final risk assessment

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for repository analysis feature)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Bug_Predictor.git
   cd Bug_Predictor
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model** (first-time setup)
   ```bash
   python train_robust_model.py
   ```

5. **Run the application**
   ```bash
   python backend/app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

---

## 📖 Usage Guide

### Method 1: 📁 Upload File

Perfect for analyzing individual source code files.

1. Click on the **"Upload File"** tab
2. Click the upload area or drag and drop your file
3. Supported formats: `.py`, `.java`, `.c`, `.cpp`, `.js`, `.php`, `.go`, `.rb`
4. Click **"Analyze File"** button
5. View detailed risk analysis and recommendations

**Example:**
```
✅ Upload: calculator.py
🔍 Analysis: Cyclomatic Complexity: 8, LOC: 150
⚠️ Risk Level: MEDIUM - Consider refactoring complex functions
```

---

### Method 2: 📝 Paste Code

Ideal for quick analysis of code snippets or functions.

1. Click on the **"Paste Code"** tab
2. Paste your code into the text area
3. Select the programming language from the dropdown
4. Click **"Analyze File"** button
5. Get instant feedback on code quality and risk

**Example Use Cases:**
- Reviewing a colleague's code snippet
- Testing a new function before committing
- Quick complexity check during development

---

### Method 3: 🔗 Git Repository

Comprehensive analysis for entire projects.

1. Click on the **"Git Repo"** tab
2. Enter the repository URL (e.g., `https://github.com/username/project`)
3. Click **"Analyze File"** button
4. Wait for the analysis to complete (may take a few minutes for large repos)
5. Review the comprehensive report with file-by-file risk assessment

**Features:**
- Analyzes all supported files in the repository
- Ranks files by risk level
- Identifies hotspots requiring immediate attention
- Generates downloadable reports

**Example:**
```
Repository: https://github.com/example/project
Files Analyzed: 47
High Risk: 3 files
Medium Risk: 12 files
Low Risk: 32 files
```

---

## 🌐 Supported Languages

Bug Predictor supports static analysis for the following programming languages:

| Language | Extension | Status |
|----------|-----------|--------|
| Python | `.py` | ✅ Full Support |
| Java | `.java` | ✅ Full Support |
| C | `.c` | ✅ Full Support |
| C++ | `.cpp`, `.cc` | ✅ Full Support |
| JavaScript | `.js` | ✅ Full Support |
| PHP | `.php` | ✅ Full Support |
| Go | `.go` | ✅ Full Support |
| Ruby | `.rb` | ✅ Full Support |

---

## 🔧 Technical Details

### Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Training Data**: NASA Promise Software Defect Dataset
- **Class Balancing**: SMOTE (Synthetic Minority Over-sampling Technique)
- **Features**: 20+ code complexity metrics

### Complexity Metrics
- **Cyclomatic Complexity**: Measures code branching complexity
- **Halstead Metrics**: Volume, difficulty, effort calculations
- **Lines of Code**: Physical and logical line counts
- **Maintainability Index**: Overall code maintainability score

### Risk Classification
- 🟢 **LOW**: Well-structured, low complexity code
- 🟡 **MEDIUM**: Moderate complexity, review recommended
- 🔴 **HIGH**: High complexity, refactoring strongly advised

---

## 📁 Project Structure

```
Bug_Predictor/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── analyzer.py            # Code analysis engine
│   ├── ml_model.py            # ML prediction logic
│   ├── templates/             # HTML templates
│   │   ├── index.html
│   │   └── result.html
│   └── tests/                 # Unit tests
├── models/
│   └── random_forest_model.pkl # Trained ML model
├── datasets/                   # NASA Promise datasets
├── train_robust_model.py      # Model training script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Soukaina** - *Initial work* - Module: Génie Logiciel

---

## 🙏 Acknowledgments

- NASA Promise Software Engineering Repository for the training datasets
- SCRUM methodology for agile development process
- Flask and scikit-learn communities for excellent documentation

---

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

**Happy Coding! 🚀**