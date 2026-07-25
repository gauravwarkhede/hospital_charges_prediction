"""
===============================================================================
MEDICO.AI - ENTERPRISE HOSPITAL CHARGES PREDICTION SYSTEM
===============================================================================
This file contains a production-ready Flask application, including:
1. Advanced Configuration & Environment Management
2. Custom Exception Handling & Error Routing
3. Enterprise Logging System (Rotating Files & Console)
4. SQLite Database Layer for Audit Trails & Prediction History
5. Authentication Middleware (API Key Verification)
6. Robust Input Validation Engine
7. Machine Learning Model Manager (Scikit-Learn Pickler & Fallback)
8. Advanced Analytics & Risk Calculation Engine
9. Comprehensive RESTful API Endpoints
10. Built-in Unit Testing Suite
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
import unittest
from functools import wraps
from logging.handlers import RotatingFileHandler

import numpy as np
from flask import Flask, render_template, request, jsonify, g, abort

# Suppress warnings for cleaner logs
warnings.filterwarnings("ignore", category=UserWarning)


# =============================================================================
# 1. CONFIGURATION & CONSTANTS
# =============================================================================

class Config:
    """Base configuration variables."""
    APP_NAME = "Medico.AI Core"
    VERSION = "2.0.0"
    MODEL_PATH = "Practice.pkl"
    DB_PATH = "medico_data.db"
    LOG_FILE = "medico_server.log"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-dev-key-12345")
    REQUIRE_AUTH = False  # Set to True to require API keys

class DevelopmentConfig(Config):
    DEBUG = True
    REQUIRE_AUTH = False

class ProductionConfig(Config):
    DEBUG = False
    REQUIRE_AUTH = True

class TestingConfig(Config):
    TESTING = True
    DB_PATH = ":memory:"  # In-memory DB for tests
    MODEL_PATH = "dummy_path.pkl"

# Feature definitions
FEATURE_NAMES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

# Categorical Mappings
SEX_MAP = {'female': 0, 'male': 1}
SMOKER_MAP = {'no': 0, 'yes': 1}
REGION_MAP = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}


# =============================================================================
# 2. CUSTOM EXCEPTIONS
# =============================================================================

class MedicoAPIException(Exception):
    """Base class for all custom API exceptions."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['error'] = self.message
        return rv

class ModelLoadError(MedicoAPIException):
    """Raised when the ML model fails to load and fallback fails."""
    def __init__(self, message="Machine learning model could not be initialized."):
        super().__init__(message, status_code=500)

class ValidationError(MedicoAPIException):
    """Raised when user input fails validation."""
    def __init__(self, message):
        super().__init__(message, status_code=422)

class UnauthorizedError(MedicoAPIException):
    """Raised when authentication fails."""
    def __init__(self, message="Invalid or missing API Key."):
        super().__init__(message, status_code=401)


# =============================================================================
# 3. ENTERPRISE LOGGING SYSTEM
# =============================================================================

class LoggerManager:
    """Manages application-wide logging with file rotation and formatting."""
    
    @staticmethod
    def setup_logger(config_class):
        logger = logging.getLogger('medico_app')
        logger.setLevel(logging.DEBUG if config_class.DEBUG else logging.INFO)
        
        # Prevent adding multiple handlers if logger already exists
        if not logger.handlers:
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s in %(module)s (Line %(lineno)d): %(message)s'
            )
            
            # File Handler
            if config_class.DB_PATH != ":memory:":
                file_handler = RotatingFileHandler(
                    config_class.LOG_FILE, maxBytes=10485760, backupCount=5
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            
            # Console Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
        return logger

app_logger = LoggerManager.setup_logger(DevelopmentConfig)


# =============================================================================
# 4. DATABASE MANAGER (SQLITE)
# =============================================================================

class DatabaseManager:
    """Handles all SQLite database connections, setups, and queries."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def _initialize_db(self):
        """Creates required tables if they do not exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Table for tracking predictions
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS predictions (
                        id TEXT PRIMARY KEY,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        age REAL,
                        sex TEXT,
                        bmi REAL,
                        children INTEGER,
                        smoker TEXT,
                        region TEXT,
                        predicted_charge REAL,
                        risk_score INTEGER,
                        risk_level TEXT
                    )
                ''')
                # Table for audit logs
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        endpoint TEXT,
                        method TEXT,
                        ip_address TEXT,
                        status_code INTEGER,
                        processing_time_ms REAL
                    )
                ''')
                conn.commit()
            app_logger.info("Database initialized successfully.")
        except Exception as e:
            app_logger.error(f"Database initialization failed: {e}")

    def save_prediction(self, data, prediction_results):
        """Saves a prediction instance to the database."""
        try:
            pred_id = str(uuid.uuid4())
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO predictions 
                    (id, age, sex, bmi, children, smoker, region, predicted_charge, risk_score, risk_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pred_id,
                    data['age'], data['sex'], data['bmi'], data['children'],
                    data['smoker'], data['region'],
                    prediction_results['charge_val'],
                    prediction_results['risk_metrics']['risk_score'],
                    prediction_results['risk_metrics']['risk_level']
                ))
                conn.commit()
            return pred_id
        except Exception as e:
            app_logger.error(f"Failed to save prediction to DB: {e}")
            return None

    def get_recent_predictions(self, limit=50):
        """Retrieves recent predictions for analytics."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?', (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            app_logger.error(f"Failed to fetch predictions from DB: {e}")
            return []

    def log_audit(self, endpoint, method, ip_address, status_code, proc_time):
        """Saves an audit trail of API requests."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO audit_logs (endpoint, method, ip_address, status_code, processing_time_ms)
                    VALUES (?, ?, ?, ?, ?)
                ''', (endpoint, method, ip_address, status_code, proc_time))
                conn.commit()
        except Exception as e:
            app_logger.error(f"Failed to log audit: {e}")

db_manager = DatabaseManager(DevelopmentConfig.DB_PATH)


# =============================================================================
# 5. MACHINE LEARNING MODEL MANAGER
# =============================================================================

class ModelManager:
    """Handles model loading, fallback generation, and preprocessing."""
    
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.is_fallback = False
        self.load_model()
        
    def load_model(self):
        """Loads Practice.pkl safely, with a robust fallback mechanism."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                
                if not hasattr(self.model, 'predict'):
                    raise ValueError("Pickle loaded, but object has no 'predict' method.")
                    
                app_logger.info(f"✅ Primary Model loaded successfully from {self.model_path}")
                self.is_fallback = False
                return
            except Exception as e:
                app_logger.warning(f"⚠️ Failed to load primary model ({e}). Initializing fallback.")
        else:
            app_logger.warning(f"⚠️ Model file '{self.model_path}' not found. Initializing fallback.")
            
        self._initialize_fallback_model()
        
    def _initialize_fallback_model(self):
        """Trains an in-memory Linear Regression model to prevent app crashes."""
        try:
            from sklearn.linear_model import LinearRegression
            
            # Synthetic dataset simulating insurance data
            X_dummy = np.array([
                [19, 0, 27.9, 0, 1, 3], [18, 1, 33.77, 1, 0, 2], [28, 1, 33.0, 3, 0, 2],
                [33, 1, 22.7, 0, 0, 1], [32, 1, 28.88, 0, 0, 1], [31, 0, 25.74, 0, 1, 2],
                [46, 0, 33.44, 1, 0, 2], [37, 0, 27.74, 3, 0, 1], [37, 1, 29.83, 2, 0, 0],
                [60, 0, 25.84, 0, 0, 1], [25, 1, 26.22, 0, 0, 0], [62, 0, 26.29, 0, 1, 2],
                [23, 1, 34.4, 0, 0, 3], [56, 0, 39.82, 0, 0, 2], [27, 1, 42.13, 0, 1, 2]
            ])
            y_dummy = np.array([
                16884.92, 1725.55, 4449.46, 21984.47, 3866.85, 37566.25, 
                8240.59, 7281.50, 6406.41, 28923.43, 2721.32, 27808.72, 
                1826.84, 11090.71, 39611.75
            ])
            
            self.model = LinearRegression()
            self.model.fit(X_dummy, y_dummy)
            self.model.feature_names_in_ = np.array(FEATURE_NAMES)
            self.is_fallback = True
            app_logger.info("✅ Fallback Linear Regression model trained and ready.")
        except ImportError:
            app_logger.critical("Scikit-learn is not installed! Application cannot function.")
            raise ModelLoadError("Scikit-learn dependency missing.")

    def preprocess(self, raw_data):
        """Cleans, validates, and encodes raw JSON data into a numpy array."""
        try:
            # 1. Validation & Extraction
            age = float(raw_data.get('age', 30))
            if not (0 <= age <= 120): raise ValueError("Age must be between 0 and 120.")
            
            sex_raw = str(raw_data.get('sex', 'male')).lower().strip()
            if sex_raw not in SEX_MAP: raise ValueError(f"Invalid sex: {sex_raw}")
            sex = SEX_MAP[sex_raw]
            
            bmi = float(raw_data.get('bmi', 25.0))
            if not (10 <= bmi <= 80): raise ValueError("BMI must be between 10 and 80.")
            
            children = int(raw_data.get('children', 0))
            if not (0 <= children <= 20): raise ValueError("Children must be between 0 and 20.")
            
            smoker_raw = str(raw_data.get('smoker', 'no')).lower().strip()
            if smoker_raw not in SMOKER_MAP: raise ValueError(f"Invalid smoker status: {smoker_raw}")
            smoker = SMOKER_MAP[smoker_raw]
            
            region_raw = str(raw_data.get('region', 'southeast')).lower().strip()
            if region_raw not in REGION_MAP: raise ValueError(f"Invalid region: {region_raw}")
            region = REGION_MAP[region_raw]
            
            features_array = np.array([[age, sex, bmi, children, smoker, region]])
            
            clean_inputs = {
                'age': age, 'sex': sex_raw, 'bmi': bmi, 
                'children': children, 'smoker': smoker_raw, 'region': region_raw
            }
            
            return features_array, clean_inputs
            
        except ValueError as ve:
            raise ValidationError(str(ve))
        except Exception as e:
            raise ValidationError(f"Unexpected input error: {str(e)}")

    def predict(self, features_array):
        """Executes prediction and ensures valid boundaries."""
        if self.model is None:
            raise ModelLoadError()
            
        raw_prediction = self.model.predict(features_array)[0]
        
        # Guardrails against negative regression outputs
        return float(max(1000.0, raw_prediction))

model_engine = ModelManager(DevelopmentConfig.MODEL_PATH)


# =============================================================================
# 6. ANALYTICS & RISK CALCULATION ENGINE
# =============================================================================

class RiskAnalyzer:
    """Calculates granular risk profiles and financial drivers."""
    
    @staticmethod
    def calculate_metrics(inputs, predicted_cost):
        age = inputs['age']
        bmi = inputs['bmi']
        is_smoker = (inputs['smoker'] == 'yes')
        children = inputs['children']
        
        # 1. Base Health Risk Scoring Engine
        risk_score = 10
        
        # Age factors
        if age > 60: risk_score += 30
        elif age > 45: risk_score += 20
        elif age > 30: risk_score += 10
        
        # BMI factors
        if bmi >= 35: risk_score += 30
        elif bmi >= 30: risk_score += 20
        elif bmi >= 25: risk_score += 10
        elif bmi < 18.5: risk_score += 15 # Underweight risk
        
        # Lifestyle factors
        if is_smoker: risk_score += 40
        if children > 3: risk_score += 5
        
        # Normalize score
        risk_score = min(100, max(0, risk_score))
        
        # Risk Categorization
        if risk_score < 25:
            risk_level, badge_color = "Low Risk", "success"
        elif risk_score < 55:
            risk_level, badge_color = "Moderate Risk", "warning"
        elif risk_score < 80:
            risk_level, badge_color = "High Risk", "danger"
        else:
            risk_level, badge_color = "Critical Risk", "critical"
            
        # 2. Financial Breakdown (Simulated Feature Importance)
        base_charge = max(1500.0, float(predicted_cost) * 0.12)
        
        # Dynamic calculation based on user inputs
        age_impact = (age / 100.0) * predicted_cost * 0.25
        bmi_impact = 0.0 if bmi < 25 else ((bmi - 25) / 30.0) * predicted_cost * 0.20
        smoker_impact = predicted_cost * 0.40 if is_smoker else 0.0
        family_impact = (children * 500.0)
        
        # Adjust rounding errors to match total exactly
        calculated_total = base_charge + age_impact + bmi_impact + smoker_impact + family_impact
        adjustment = predicted_cost - calculated_total
        base_charge += adjustment # Fold remainder into base charge
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'badge_color': badge_color,
            'breakdown': {
                'Base Hospital Fee': round(base_charge, 2),
                'Age Surcharge': round(age_impact, 2),
                'BMI Risk Factor': round(bmi_impact, 2),
                'Tobacco Surcharge': round(smoker_impact, 2),
                'Dependents Coverage': round(family_impact, 2)
            }
        }


# =============================================================================
# 7. FLASK APPLICATION FACTORY
# =============================================================================

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# =============================================================================
# 8. MIDDLEWARE & BEFORE/AFTER REQUEST HANDLERS
# =============================================================================

@app.before_request
def start_timer():
    """Start timer to track endpoint processing time."""
    g.start_time = time.time()

@app.before_request
def check_authentication():
    """Validates API Keys if authentication is required by config."""
    if app.config['REQUIRE_AUTH']:
        # Skip auth for frontend routes
        if request.endpoint and request.endpoint.startswith('api_'):
            api_key = request.headers.get('X-API-KEY')
            # Mock secure token check
            valid_tokens = ["medico-admin-777", "medico-dev-123"]
            if not api_key or api_key not in valid_tokens:
                raise UnauthorizedError("Valid X-API-KEY header is required.")

@app.after_request
def log_response(response):
    """Logs the request details and execution time to the audit database."""
    if hasattr(g, 'start_time'):
        proc_time = round((time.time() - g.start_time) * 1000, 2)
        
        # Skip static file logging
        if request.endpoint and 'static' not in request.endpoint:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            # Console Log
            app_logger.info(f"{request.method} {request.path} - {response.status_code} - {proc_time}ms")
            
            # DB Audit Log
            db_manager.log_audit(
                endpoint=request.path,
                method=request.method,
                ip_address=ip,
                status_code=response.status_code,
                proc_time=proc_time
            )
            
    # CORS Headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-KEY'
    return response


# =============================================================================
# 9. ERROR HANDLING MIDDLEWARE
# =============================================================================

@app.errorhandler(MedicoAPIException)
def handle_api_exception(error):
    app_logger.warning(f"API Exception: {error.message}")
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({'success': False, 'error': 'Endpoint not found.'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'success': False, 'error': 'HTTP method not allowed for this endpoint.'}), 405

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app_logger.error(f"UNEXPECTED ERROR: {str(error)}\n{traceback.format_exc()}")
    return jsonify({
        'success': False, 
        'error': 'Internal server error occurred.',
        'details': str(error) if app.config['DEBUG'] else None
    }), 500


# =============================================================================
# 10. FRONTEND ROUTES
# =============================================================================

@app.route('/', methods=['GET'])
def index():
    """Serves the main frontend Single Page Application (SPA)."""
    return render_template('index.html')


# =============================================================================
# 11. API ROUTES (V1)
# =============================================================================

@app.route('/api/v1/health', methods=['GET'], endpoint='api_health')
def health_check():
    """Deep system health check (Model status, DB status)."""
    db_status = "Healthy"
    try:
        db_manager.get_connection().execute("SELECT 1").fetchone()
    except Exception:
        db_status = "Failed"
        
    return jsonify({
        'success': True,
        'status': 'Online',
        'version': app.config['VERSION'],
        'model_loaded': model_engine.model is not None,
        'is_fallback_model': model_engine.is_fallback,
        'database_status': db_status,
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

@app.route('/predict', methods=['POST'], endpoint='api_predict')
def make_prediction():
    """Core prediction endpoint. Processes data, predicts, logs, and returns stats."""
    
    # 1. Extract Payload
    data = request.get_json(force=True, silent=True)
    if not data:
        raise ValidationError("Invalid JSON payload or empty request body.")
        
    # 2. Preprocess & Validate
    features_array, clean_inputs = model_engine.preprocess(data)
    
    # 3. Predict Output
    estimated_charge = model_engine.predict(features_array)
    
    # 4. Generate Risk Analytics
    analysis = RiskAnalyzer.calculate_metrics(clean_inputs, estimated_charge)
    
    # 5. Format Output
    formatted_charge = f"${estimated_charge:,.2f}"
    
    result_payload = {
        'success': True,
        'predicted_charge': formatted_charge,
        'charge_val': round(estimated_charge, 2),
        'risk_metrics': analysis,
        'inputs': clean_inputs,
        'model_info': {
            'is_fallback': model_engine.is_fallback,
            'features_used': FEATURE_NAMES
        }
    }
    
    # 6. Save to Database
    pred_id = db_manager.save_prediction(clean_inputs, result_payload)
    if pred_id:
        result_payload['prediction_id'] = pred_id
        
    return jsonify(result_payload), 200


@app.route('/api/analytics', methods=['GET'], endpoint='api_analytics_dashboard')
def get_dashboard_analytics():
    """Aggregates database records and synthetic data for the frontend dashboards."""
    
    # Generate synthetic curve data for smooth chart rendering
    ages = list(range(18, 65, 4))
    avg_non_smoker = [2500 + (a**1.35) * 40 for a in ages]
    avg_smoker = [16000 + (a**1.4) * 55 for a in ages]
    
    # Calculate regional aggregates from the database if available
    recent_records = db_manager.get_recent_predictions(limit=100)
    
    regional_data = {'Northeast': 0, 'Northwest': 0, 'Southeast': 0, 'Southwest': 0}
    regional_counts = {'Northeast': 0, 'Northwest': 0, 'Southeast': 0, 'Southwest': 0}
    
    for record in recent_records:
        region = record['region'].capitalize()
        if region in regional_data:
            regional_data[region] += record['predicted_charge']
            regional_counts[region] += 1
            
    # Calculate averages, fallback to defaults if DB is empty
    default_regional = {
        'Northeast': 13406.12, 'Northwest': 12417.58, 
        'Southeast': 14735.41, 'Southwest': 12346.94
    }
    
    for reg in regional_data:
        if regional_counts[reg] > 0:
            regional_data[reg] = round(regional_data[reg] / regional_counts[reg], 2)
        else:
            regional_data[reg] = default_regional[reg]

    return jsonify({
        'success': True,
        'age_trend': {
            'labels': ages,
            'non_smoker_cost': avg_non_smoker,
            'smoker_cost': avg_smoker
        },
        'regional_costs': regional_data,
        'total_historical_predictions': len(recent_records)
    }), 200


@app.route('/api/v1/database/export', methods=['GET'], endpoint='api_db_export')
def export_database():
    """Exports prediction history for data science teams. Requires API Key."""
    # Force Auth for this specific sensitive endpoint
    api_key = request.headers.get('X-API-KEY')
    if api_key != "admin-export-key-999":
        raise UnauthorizedError("High-level admin API Key required for data export.")
        
    records = db_manager.get_recent_predictions(limit=1000)
    return jsonify({
        'success': True,
        'count': len(records),
        'data': records
    }), 200


# =============================================================================
# 12. UNIT TESTING SUITE (Built-In)
# =============================================================================
# This allows you to run `python app.py --test` to verify all components.

class MedicoAppTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and in-memory database before each test."""
        app.config.from_object(TestingConfig)
        self.client = app.test_client()
        # Overwrite global db_manager for testing
        global db_manager
        db_manager = DatabaseManager(":memory:")
        
    def test_health_check(self):
        """Verify the health endpoint responds correctly."""
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['database_status'], 'Healthy')
        
    def test_prediction_valid_input(self):
        """Verify the prediction engine works with correct data."""
        payload = {
            "age": 35, "sex": "female", "bmi": 26.5, 
            "children": 2, "smoker": "no", "region": "northeast"
        }
        response = self.client.post('/predict', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('predicted_charge', data)
        self.assertEqual(data['risk_metrics']['risk_level'], 'Moderate Risk')
        
    def test_prediction_invalid_age(self):
        """Verify validation blocks impossible ages."""
        payload = {"age": -5, "sex": "male"}
        response = self.client.post('/predict', json=payload)
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Age must be between 0 and 120', data['error'])
        
    def test_analytics_dashboard(self):
        """Verify the analytics data formatting."""
        response = self.client.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('regional_costs', data)
        self.assertIn('age_trend', data)

    def test_database_insertion(self):
        """Verify predictions are saved to the local SQLite DB."""
        payload = {
            "age": 45, "sex": "male", "bmi": 32.1, 
            "children": 0, "smoker": "yes", "region": "southwest"
        }
        self.client.post('/predict', json=payload)
        records = db_manager.get_recent_predictions()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['smoker'], 'yes')
        self.assertEqual(records[0]['age'], 45.0)


# =============================================================================
# 13. MAIN EXECUTION BLOCK
# =============================================================================

if __name__ == '__main__':
    
    # Check for CLI test flag
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        app_logger.info("Starting Unit Testing Suite...")
        # Remove the flag so unittest doesn't get confused
        sys.argv.pop()
        unittest.main()
    else:
        app_logger.info(f"Starting {app.config['APP_NAME']} v{app.config['VERSION']}")
        app_logger.info("Initializing embedded server...")
        
        # Run Flask server
        # 'threaded=True' allows multiple concurrent requests
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=app.config['DEBUG'],
            threaded=True 
        )
