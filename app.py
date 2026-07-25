"""
===============================================================================
MEDICO.AI - SINGLE-FILE ENTERPRISE APPLICATION
===============================================================================
This file contains the entire application (Backend, Database, Model, and Frontend UI).
No 'templates' folder is required.
===============================================================================
"""

import os
import sys
import json
import time
import uuid
import pickle
import sqlite3
import logging
import datetime
import warnings
import traceback
import numpy as np
from flask import Flask, request, jsonify, g, render_template_string

warnings.filterwarnings("ignore", category=UserWarning)

# =============================================================================
# 1. FRONTEND UI EMBEDDED (HTML/CSS/JS)
# =============================================================================
# We embed the UI as a string to avoid the TemplateNotFound folder error.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="cyberpunk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Charges Prediction & Analytics Core</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #0b0f19;
            --bg-card: rgba(18, 26, 43, 0.65);
            --border-glow: rgba(0, 240, 255, 0.25);
            --accent-primary: #00f0ff;
            --accent-secondary: #7000ff;
            --accent-tertiary: #ff007f;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --font-head: 'Orbitron', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
            --glass-blur: blur(16px);
            --card-radius: 20px;
            --transition-smooth: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* THEMES */
        [data-theme="cyberpunk"] { --bg-base: #080c14; --bg-card: rgba(13, 20, 36, 0.7); --border-glow: rgba(0, 240, 255, 0.3); --accent-primary: #00f0ff; --accent-secondary: #8b5cf6; --accent-tertiary: #ec4899; --text-main: #f8fafc; --text-muted: #64748b; }
        [data-theme="solar-golden"] { --bg-base: #0f0d0a; --bg-card: rgba(28, 23, 16, 0.75); --border-glow: rgba(245, 158, 11, 0.35); --accent-primary: #f59e0b; --accent-secondary: #d97706; --accent-tertiary: #ef4444; --text-main: #fffbeb; --text-muted: #a1a1aa; }
        [data-theme="purple-magic"] { --bg-base: #0e0a1a; --bg-card: rgba(25, 18, 45, 0.75); --border-glow: rgba(168, 85, 247, 0.35); --accent-primary: #a855f7; --accent-secondary: #c084fc; --accent-tertiary: #e879f9; --text-main: #faf5ff; --text-muted: #988aae; }
        [data-theme="ice-sapphire"] { --bg-base: #06111e; --bg-card: rgba(12, 30, 52, 0.7); --border-glow: rgba(56, 189, 248, 0.35); --accent-primary: #38bdf8; --accent-secondary: #0284c7; --accent-tertiary: #818cf8; --text-main: #f0f9ff; --text-muted: #64748b; }
        [data-theme="emerald-bio"] { --bg-base: #04140d; --bg-card: rgba(10, 36, 24, 0.75); --border-glow: rgba(16, 185, 129, 0.35); --accent-primary: #10b981; --accent-secondary: #059669; --accent-tertiary: #34d399; --text-main: #ecfdf5; --text-muted: #6ee7b7; }
        [data-theme="crimson-velvet"] { --bg-base: #14060a; --bg-card: rgba(36, 12, 18, 0.75); --border-glow: rgba(244, 63, 94, 0.35); --accent-primary: #f43f5e; --accent-secondary: #e11d48; --accent-tertiary: #fb7185; --text-main: #fff1f2; --text-muted: #fda4af; }
        [data-theme="deep-space"] { --bg-base: #030308; --bg-card: rgba(15, 15, 32, 0.8); --border-glow: rgba(99, 102, 241, 0.35); --accent-primary: #6366f1; --accent-secondary: #4f46e5; --accent-tertiary: #38bdf8; --text-main: #eef2ff; --text-muted: #818cf8; }
        [data-theme="sunset-synth"] { --bg-base: #120a17; --bg-card: rgba(32, 16, 42, 0.75); --border-glow: rgba(249, 115, 22, 0.35); --accent-primary: #f97316; --accent-secondary: #ec4899; --accent-tertiary: #8b5cf6; --text-main: #fff7ed; --text-muted: #fdba74; }
        [data-theme="matrix-obsidian"] { --bg-base: #050a05; --bg-card: rgba(10, 25, 12, 0.8); --border-glow: rgba(34, 197, 94, 0.35); --accent-primary: #22c55e; --accent-secondary: #16a34a; --accent-tertiary: #4ade80; --text-main: #f0fdf4; --text-muted: #86efac; }
        [data-theme="solar-light"] { --bg-base: #f1f5f9; --bg-card: rgba(255, 255, 255, 0.85); --border-glow: rgba(14, 165, 233, 0.3); --accent-primary: #0284c7; --accent-secondary: #6366f1; --accent-tertiary: #0d9488; --text-main: #0f172a; --text-muted: #475569; }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg-base); color: var(--text-main); font-family: var(--font-body); min-height: 100vh; overflow-x: hidden; background-image: radial-gradient(circle at 15% 15%, rgba(0, 240, 255, 0.08) 0%, transparent 40%), radial-gradient(circle at 85% 85%, rgba(120, 0, 255, 0.08) 0%, transparent 40%); transition: var(--transition-smooth); }
        header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 5%; background: rgba(10, 15, 26, 0.6); backdrop-filter: var(--glass-blur); border-bottom: 1px solid var(--border-glow); position: sticky; top: 0; z-index: 100; }
        .brand { display: flex; align-items: center; gap: 12px; font-family: var(--font-head); font-size: 1.35rem; font-weight: 800; }
        .brand-logo { width: 44px; height: 44px; background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #fff; box-shadow: 0 0 20px var(--border-glow); animation: pulseGlow 3s infinite alternate; }
        @keyframes pulseGlow { 0% { box-shadow: 0 0 15px var(--border-glow); } 100% { box-shadow: 0 0 28px var(--accent-primary); } }
        .theme-selector-wrapper { display: flex; align-items: center; gap: 10px; }
        .theme-select { background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border-glow); padding: 0.6rem 1rem; border-radius: 10px; font-weight: 600; cursor: pointer; backdrop-filter: var(--glass-blur); outline: none; }
        .container { max-width: 1400px; margin: 2rem auto; padding: 0 1.5rem; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        @media (max-width: 1024px) { .container { grid-template-columns: 1fr; } }
        .page-title { grid-column: 1 / -1; text-align: center; margin-bottom: 0.5rem; }
        .page-title h1 { font-family: var(--font-head); font-size: 2.3rem; text-transform: uppercase; background: linear-gradient(90deg, var(--accent-primary), #fff, var(--accent-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .glass-card { background: var(--bg-card); backdrop-filter: var(--glass-blur); border: 1px solid var(--border-glow); border-radius: var(--card-radius); padding: 1.8rem; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); transition: var(--transition-smooth); }
        .card-header { display: flex; align-items: center; gap: 12px; font-family: var(--font-head); font-size: 1.15rem; margin-bottom: 1.5rem; color: var(--accent-primary); border-bottom: 1px dashed var(--border-glow); padding-bottom: 0.8rem; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-group.full-width { grid-column: 1 / -1; }
        label { font-size: 0.85rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }
        input, select { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); padding: 0.75rem 1rem; border-radius: 12px; color: var(--text-main); font-family: var(--font-body); outline: none; }
        .slider-wrapper { display: flex; align-items: center; gap: 12px; }
        .slider-wrapper input[type="range"] { flex: 1; accent-color: var(--accent-primary); }
        .slider-val { font-family: var(--font-head); font-weight: 700; color: var(--accent-primary); }
        .btn-predict { width: 100%; grid-column: 1 / -1; padding: 1rem; border: none; border-radius: 14px; background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)); color: #fff; font-family: var(--font-head); font-size: 1.05rem; font-weight: 700; cursor: pointer; transition: var(--transition-smooth); }
        .result-box { text-align: center; padding: 1.5rem; border-radius: 16px; background: rgba(0, 0, 0, 0.25); border: 1px solid var(--border-glow); margin-bottom: 1.5rem; }
        .result-value { font-family: var(--font-head); font-size: 2.8rem; font-weight: 900; color: var(--accent-primary); margin: 0.3rem 0; }
        .risk-badge { display: inline-block; padding: 0.4rem 1.2rem; border-radius: 30px; font-family: var(--font-head); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
        .risk-badge.success { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
        .risk-badge.warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
        .risk-badge.danger { background: rgba(244, 63, 94, 0.2); color: #f43f5e; border: 1px solid #f43f5e; }
        .risk-badge.critical { background: rgba(239, 68, 68, 0.3); color: #ff0055; border: 1px solid #ff0055; }
        .breakdown-item { display: flex; justify-content: space-between; padding: 0.7rem 1rem; background: rgba(255, 255, 255, 0.03); border-radius: 10px; margin-bottom: 8px; border-left: 3px solid var(--accent-primary); }
        .dashboard-grid { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
        .chart-container { position: relative; height: 280px; width: 100%; }
        footer { grid-column: 1 / -1; text-align: center; padding: 2rem 0; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border-glow); margin-top: 2rem; }
    </style>
</head>
<body>
    <header>
        <div class="brand"><div class="brand-logo"><i class="fa-solid fa-notes-medical"></i></div><span>MEDICO<span style="color:var(--accent-primary)">.AI</span></span></div>
        <div class="theme-selector-wrapper">
            <i class="fa-solid fa-palette" style="color: var(--accent-primary)"></i>
            <select id="themeSelect" class="theme-select" onchange="changeTheme(this.value)">
                <option value="cyberpunk">1. Cyberpunk</option>
                <option value="solar-golden">2. Solar Golden</option>
                <option value="purple-magic">3. Purple Magic</option>
                <option value="ice-sapphire">4. Ice Sapphire</option>
                <option value="emerald-bio">5. Emerald Bio</option>
                <option value="crimson-velvet">6. Crimson Velvet</option>
                <option value="deep-space">7. Deep Space</option>
                <option value="sunset-synth">8. Sunset Synth</option>
                <option value="matrix-obsidian">9. Matrix</option>
                <option value="solar-light">10. Solar Light</option>
            </select>
        </div>
    </header>

    <main class="container">
        <div class="page-title">
            <h1>The Charges Prediction of Hospital</h1>
            <p>Futuristic AI Medical Cost Estimation & Predictive Health Analytics Engine</p>
        </div>

        <section class="glass-card">
            <div class="card-header"><i class="fa-solid fa-sliders"></i><span>Patient Input Parameters</span></div>
            <form id="predictionForm" onsubmit="handlePrediction(event)">
                <div class="form-grid">
                    <div class="form-group full-width">
                        <label>Age: <span id="ageVal" class="slider-val">35</span> yrs</label>
                        <div class="slider-wrapper"><input type="range" id="age" min="18" max="100" value="35" oninput="document.getElementById('ageVal').innerText = this.value"></div>
                    </div>
                    <div class="form-group">
                        <label>Sex</label>
                        <select id="sex"><option value="male">Male</option><option value="female">Female</option></select>
                    </div>
                    <div class="form-group">
                        <label>Smoker</label>
                        <select id="smoker"><option value="no">No</option><option value="yes">Yes</option></select>
                    </div>
                    <div class="form-group full-width">
                        <label>BMI: <span id="bmiVal" class="slider-val">26.5</span></label>
                        <div class="slider-wrapper"><input type="range" id="bmi" min="15.0" max="55.0" step="0.1" value="26.5" oninput="document.getElementById('bmiVal').innerText = this.value"></div>
                    </div>
                    <div class="form-group">
                        <label>Children</label>
                        <input type="number" id="children" min="0" max="10" value="1">
                    </div>
                    <div class="form-group">
                        <label>Region</label>
                        <select id="region">
                            <option value="southeast">Southeast</option>
                            <option value="southwest">Southwest</option>
                            <option value="northeast">Northeast</option>
                            <option value="northwest">Northwest</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-predict" id="predictBtn">Predict Charges</button>
                </div>
            </form>
        </section>

        <section class="glass-card">
            <div class="card-header"><i class="fa-solid fa-chart-line"></i><span>Prediction Output</span></div>
            <div class="result-box">
                <div style="color: var(--text-muted)">Estimated Hospital Charge</div>
                <div class="result-value" id="costOutput">---</div>
                <div id="riskBadge" class="risk-badge warning" style="display:none;">---</div>
            </div>
            <div id="breakdownList"></div>
        </section>

        <div class="dashboard-grid">
            <div class="glass-card">
                <div class="card-header"><i class="fa-solid fa-chart-column"></i><span>Regional Analytics</span></div>
                <div class="chart-container"><canvas id="regionalChart"></canvas></div>
            </div>
            <div class="glass-card">
                <div class="card-header"><i class="fa-solid fa-chart-area"></i><span>Age Trend Curve</span></div>
                <div class="chart-container"><canvas id="ageTrendChart"></canvas></div>
            </div>
        </div>
    </main>
    <footer><p>&copy; 2026 Medico.AI Single-File Engine.</p></footer>

    <script>
        let regChart = null; let ageChart = null;
        function changeTheme(theme) { document.documentElement.setAttribute('data-theme', theme); loadAnalytics(); }
        
        async function handlePrediction(e) {
            e.preventDefault();
            const payload = {
                age: document.getElementById('age').value, sex: document.getElementById('sex').value,
                bmi: document.getElementById('bmi').value, children: document.getElementById('children').value,
                smoker: document.getElementById('smoker').value, region: document.getElementById('region').value
            };
            try {
                const res = await fetch('/predict', { method: 'POST', body: JSON.stringify(payload) });
                const data = await res.json();
                if(data.success) {
                    document.getElementById('costOutput').innerText = data.predicted_charge;
                    const badge = document.getElementById('riskBadge');
                    badge.style.display = 'inline-block';
                    badge.innerText = `${data.risk_metrics.risk_level} Score: ${data.risk_metrics.risk_score}`;
                    badge.className = `risk-badge ${data.risk_metrics.badge_color}`;
                    
                    let html = '';
                    for (const [key, val] of Object.entries(data.risk_metrics.breakdown)) {
                        html += `<div class="breakdown-item"><span>${key}</span><strong>$${val.toLocaleString()}</strong></div>`;
                    }
                    document.getElementById('breakdownList').innerHTML = html;
                } else alert('Error: ' + data.error);
            } catch(err) { alert('Connection error'); }
        }

        async function loadAnalytics() {
            const res = await fetch('/api/analytics');
            const data = await res.json();
            const prim = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim();
            const tert = getComputedStyle(document.documentElement).getPropertyValue('--accent-tertiary').trim();
            
            if(regChart) regChart.destroy();
            if(ageChart) ageChart.destroy();

            regChart = new Chart(document.getElementById('regionalChart'), {
                type: 'bar', data: { labels: Object.keys(data.regional_costs), datasets: [{ data: Object.values(data.regional_costs), backgroundColor: prim }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            ageChart = new Chart(document.getElementById('ageTrendChart'), {
                type: 'line', data: { labels: data.age_trend.labels, datasets: [{ label: 'Smoker', data: data.age_trend.smoker_cost, borderColor: tert }, { label: 'Non-Smoker', data: data.age_trend.non_smoker_cost, borderColor: prim }] },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }
        window.onload = loadAnalytics;
    </script>
</body>
</html>
"""

# =============================================================================
# 2. CONFIGURATION & CONSTANTS
# =============================================================================

MODEL_PATH = "Practice.pkl"
DB_PATH = "medico_data.db"
FEATURE_NAMES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

SEX_MAP = {'female': 0, 'male': 1}
SMOKER_MAP = {'no': 0, 'yes': 1}
REGION_MAP = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}


# =============================================================================
# 3. DATABASE MANAGER (SQLITE)
# =============================================================================

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def _initialize_db(self):
        try:
            with self.get_connection() as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
                        id TEXT PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        age REAL, sex TEXT, bmi REAL, children INTEGER, smoker TEXT, 
                        region TEXT, predicted_charge REAL)''')
                conn.commit()
        except Exception as e:
            print(f"Database error: {e}")

    def save_prediction(self, data, charge):
        try:
            with self.get_connection() as conn:
                conn.execute('''INSERT INTO predictions (id, age, sex, bmi, children, smoker, region, predicted_charge)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                             (str(uuid.uuid4()), data['age'], data['sex'], data['bmi'], 
                              data['children'], data['smoker'], data['region'], charge))
                conn.commit()
        except Exception as e:
            print(f"Failed to save prediction: {e}")

db_manager = DatabaseManager(DB_PATH)


# =============================================================================
# 4. MACHINE LEARNING MODEL MANAGER
# =============================================================================

class ModelManager:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print(f"✅ Loaded Primary Model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Could not load {MODEL_PATH}. Using Fallback. Error: {e}")
        else:
            print(f"⚠️ {MODEL_PATH} not found. Using Fallback.")
            
        # Fallback Engine
        from sklearn.linear_model import LinearRegression
        X = np.array([[19,0,27.9,0,1,3], [18,1,33.7,1,0,2], [28,1,33.0,3,0,2], [33,1,22.7,0,0,1], [31,0,25.7,0,1,2]])
        y = np.array([16884, 1725, 4449, 21984, 37566])
        self.model = LinearRegression().fit(X, y)

    def preprocess(self, raw_data):
        age = float(raw_data.get('age', 30))
        sex = SEX_MAP.get(str(raw_data.get('sex')).lower(), 1)
        bmi = float(raw_data.get('bmi', 25.0))
        children = int(raw_data.get('children', 0))
        smoker = SMOKER_MAP.get(str(raw_data.get('smoker')).lower(), 0)
        region = REGION_MAP.get(str(raw_data.get('region')).lower(), 2)
        
        return np.array([[age, sex, bmi, children, smoker, region]]), {
            'age': age, 'sex': raw_data.get('sex'), 'bmi': bmi, 
            'children': children, 'smoker': raw_data.get('smoker'), 'region': raw_data.get('region')
        }

    def predict(self, features):
        return float(max(1000.0, self.model.predict(features)[0]))

model_engine = ModelManager()


# =============================================================================
# 5. RISK ENGINE & FLASK SETUP
# =============================================================================

def calculate_risk(inputs, charge):
    score = 10 + (30 if inputs['age'] > 50 else 10) + (20 if inputs['bmi'] > 30 else 0) + (40 if inputs['smoker'] == 'yes' else 0)
    score = min(100, score)
    color = "success" if score < 30 else "warning" if score < 70 else "danger"
    
    return {
        'risk_score': score, 'risk_level': "High" if score > 70 else "Moderate" if score > 30 else "Low", 'badge_color': color,
        'breakdown': {
            'Base Fee': round(charge * 0.15, 2),
            'Age Impact': round(inputs['age'] * 150, 2),
            'BMI Surcharge': round(max(0, inputs['bmi'] - 25) * 200, 2),
            'Lifestyle': round(15000 if inputs['smoker'] == 'yes' else 0, 2)
        }
    }

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Renders the HTML directly from the string variable above
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.get_json(force=True)
        features, clean = model_engine.preprocess(data)
        charge = model_engine.predict(features)
        db_manager.save_prediction(clean, charge)
        
        return jsonify({
            'success': True,
            'predicted_charge': f"${charge:,.2f}",
            'risk_metrics': calculate_risk(clean, charge)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/analytics', methods=['GET'])
def analytics():
    ages = list(range(18, 65, 4))
    return jsonify({
        'regional_costs': {'Northeast': 13406, 'Northwest': 12417, 'Southeast': 14735, 'Southwest': 12346},
        'age_trend': {
            'labels': ages,
            'non_smoker_cost': [2500 + (a**1.35) * 40 for a in ages],
            'smoker_cost': [16000 + (a**1.4) * 55 for a in ages]
        }
    })

if __name__ == '__main__':
    print("🚀 Server starting! Go to http://127.0.0.1:5000 in your browser.")
    app.run(host='0.0.0.0', port=5000, debug=True)
