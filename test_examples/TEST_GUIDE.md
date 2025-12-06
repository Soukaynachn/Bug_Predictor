# 🧪 Guide de Test - Bug Predictor

## Exemples de Fichiers de Test

J'ai créé deux fichiers Python pour tester le système :

### 1. 📗 `simple_code.py` - **LOW RISK attendu**
- **Caractéristiques** :
  - ~30 lignes de code
  - Complexité cyclomatique faible (~1-2 par fonction)
  - Fonctions simples sans imbrication
  - Peu de conditions if/else
  
- **Résultat attendu** : 
  - Risk Score : **< 0.3** (Low Risk)
  - Couleur : **Vert**

### 2. 📕 `complex_code.py` - **HIGH RISK attendu**
- **Caractéristiques** :
  - ~160 lignes de code
  - Complexité cyclomatique élevée (~15-20)
  - Nombreuses imbrications (if dans if dans for)
  - Multiples try/except
  - Nombreuses branches conditionnelles
  
- **Résultat attendu** :
  - Risk Score : **> 0.6** (High Risk)
  - Couleur : **Rouge**

---

## 🚀 Comment Tester

### Option 1 : Upload de Fichier
1. Allez sur `http://127.0.0.1:5000/`
2. Cliquez sur l'onglet **"📁 Upload File"**
3. Sélectionnez `test_examples/simple_code.py`
4. Cliquez sur **"🔍 Analyze File"**
5. Vérifiez que le score est **LOW RISK**
6. Répétez avec `complex_code.py` → devrait être **HIGH RISK**

### Option 2 : Copier-Coller
1. Allez sur `http://127.0.0.1:5000/`
2. Cliquez sur l'onglet **"📝 Paste Code"**
3. Ouvrez `test_examples/simple_code.py` et copiez tout le contenu
4. Collez dans la zone de texte
5. Cliquez sur **"🔍 Analyze Code"**
6. Vérifiez le résultat

---

## 📊 Métriques à Observer

Pour chaque test, vous verrez :

### Métriques Extraites
- **LOC** (Lines of Code) : Nombre de lignes
- **SLOC** (Source Lines of Code) : Lignes sans commentaires/blancs
- **Cyclomatic Complexity** : Complexité du code (nombre de chemins)
- **Halstead Volume** : Mesure de la taille du programme

### Prédiction
- **Risk Prediction** : High Risk / Low Risk
- **Probability** : Pourcentage de probabilité de bug (0-100%)

---

## ✅ Résultats Attendus

| Fichier | LOC | Complexité | Risk Score | Verdict |
|---------|-----|------------|------------|---------|
| `simple_code.py` | ~30 | ~1-2 | < 30% | ✅ Low Risk |
| `complex_code.py` | ~160 | ~15-20 | > 60% | ⚠️ High Risk |

---

## 🔍 Vérification du Modèle

Au démarrage du serveur, vérifiez :
```
🚀 Loading trained model...
✅ Model loaded successfully with 32 features
📅 Model last updated: 2025-12-04 20:XX:XX
```

Si la date est récente (aujourd'hui), le modèle mis à jour est bien utilisé !

---

## 🐛 Dépannage

**Si tous les scores sont identiques** :
- Redémarrez le serveur (`Ctrl+C` puis `python backend/app.py`)
- Vérifiez que `models/model.pkl` existe et est récent

**Si erreur "Failed to extract features"** :
- Vérifiez que le code est du Python valide
- Essayez avec les exemples fournis d'abord
