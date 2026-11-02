import os
import csv
import pickle
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'patient_feedback_sentiment_analyzer_secret_key'

# File paths
USERS_CSV = 'users.csv'
FEEDBACK_CSV = 'feedback.csv'
MODEL_PATH = 'model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

# Doctor and Department Mapping
DEPT_DOCTORS = {
    "Cardiology": ["Dr. Ravi", "Dr. Sharma"],
    "Pediatrics": ["Dr. Mehta", "Dr. Patel"],
    "Orthopedics": ["Dr. Verma", "Dr. Nair"],
    "General Medicine": ["Dr. Gupta", "Dr. Joshi"],
    "Dentist": ["Dr. Dhoni", "Dr.Kohli"]
}

# Initialize CSV Databases
def init_databases():
    # Setup users.csv
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['full_name', 'email', 'password_hash', 'role'])
        
        # Seed default Admin
        admin_hash = generate_password_hash('admin123')
        with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Admin User', 'admin@hospital.com', admin_hash, 'admin'])
        print("users.csv initialized and admin seeded.")

    # Setup feedback.csv
    if not os.path.exists(FEEDBACK_CSV):
        with open(FEEDBACK_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'user_name', 'hospital', 'doctor', 'department', 
                'date', 'feedback', 'predicted_sentiment', 
                'confidence_score', 'timestamp'
            ])
        print("feedback.csv initialized.")

init_databases()

# Load ML Model
def load_ml_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        # Fallback if train_model.py wasn't run yet
        print("Model and vectorizer not found. Running training script...")
        import subprocess
        # Execute training script in this virtualenv context
        python_exe = os.path.join('venv', 'Scripts', 'python.exe')
        if not os.path.exists(python_exe):
            python_exe = 'python' # fallback
        subprocess.run([python_exe, 'train_model.py'], check=True)
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

try:
    model, vectorizer = load_ml_model()
except Exception as e:
    print(f"Error loading model: {e}")
    model, vectorizer = None, None

# CSV Helper Functions
def get_all_users():
    users = []
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    return users

def get_user_by_email(email):
    users = get_all_users()
    for user in users:
        if user['email'].lower() == email.lower():
            return user
    return None

def add_user(full_name, email, password_hash, role='user'):
    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([full_name, email, password_hash, role])

def update_user_profile(email, new_name, new_password_hash=None):
    users = get_all_users()
    updated = False
    with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['full_name', 'email', 'password_hash', 'role'])
        for u in users:
            if u['email'].lower() == email.lower():
                u['full_name'] = new_name
                if new_password_hash:
                    u['password_hash'] = new_password_hash
                updated = True
            writer.writerow([u['full_name'], u['email'], u['password_hash'], u['role']])
    return updated

def get_all_feedback():
    feedbacks = []
    if os.path.exists(FEEDBACK_CSV):
        with open(FEEDBACK_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                feedbacks.append(row)
    return feedbacks

def add_feedback(user_name, hospital, doctor, department, date, feedback, predicted_sentiment, confidence_score):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(FEEDBACK_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            user_name, hospital, doctor, department, date, 
            feedback, predicted_sentiment, confidence_score, timestamp
        ])

# Decorators for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'email' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash("Please fill in all fields.", "danger")
            return render_template('login.html')
            
        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['email'] = user['email']
            session['name'] = user['full_name']
            session['role'] = user['role']
            flash(f"Welcome back, {user['full_name']}!", "success")
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not full_name or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template('register.html')
            
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')
            
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('login'))
            
        password_hash = generate_password_hash(password)
        add_user(full_name, email, password_hash, role='user')
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    hospitals = ["Apollo Hospital", "JSS Hospital", "Manipal Hospital", "Fortis Hospital"]
    departments = list(DEPT_DOCTORS.keys())
    
    datetime_now = datetime.now().strftime('%d %B %Y, %I:%M %p')
    current_date_str = datetime.now().strftime('%Y-%m-%d')
    
    return render_template(
        'dashboard.html', 
        hospitals=hospitals, 
        departments=departments, 
        dept_doctors=DEPT_DOCTORS,
        datetime_now=datetime_now,
        current_date_str=current_date_str
    )

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    global model, vectorizer
    if model is None or vectorizer is None:
        try:
            model, vectorizer = load_ml_model()
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'ML model not loaded: {str(e)}'}), 500
            
    hospital = request.form.get('hospital')
    doctor = request.form.get('doctor')
    department = request.form.get('department')
    date_visit = request.form.get('date_visit')
    feedback_text = request.form.get('feedback', '').strip()
    
    if not all([hospital, doctor, department, date_visit, feedback_text]):
        return jsonify({'status': 'error', 'message': 'All form fields are required.'}), 400
        
    try:
        # Sentiment prediction
        vec_text = vectorizer.transform([feedback_text])
        prediction = model.predict(vec_text)[0]
        
        # Calculate confidence
        probs = model.predict_proba(vec_text)[0]
        classes = list(model.classes_)
        pred_idx = classes.index(prediction)
        confidence = float(probs[pred_idx])
        confidence_percent = int(round(confidence * 100))
        
        # Save to database CSV
        add_feedback(
            user_name=session.get('name'),
            hospital=hospital,
            doctor=doctor,
            department=department,
            date=date_visit,
            feedback=feedback_text,
            predicted_sentiment=prediction,
            confidence_score=f"{confidence_percent}%"
        )
        
        # Emoji and label mapping
        emoji = "😊" if prediction.lower() == 'positive' else "😟"
        
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'confidence': confidence_percent,
            'emoji': emoji
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error in model prediction: {str(e)}'}), 500

@app.route('/history')
@login_required
def history():
    all_feedbacks = get_all_feedback()
    # Filter for logged-in user
    user_feedbacks = [f for f in all_feedbacks if f['user_name'] == session.get('name')]
    # Sort history by timestamp descending
    user_feedbacks.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return render_template('history.html', feedbacks=user_feedbacks)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_user_by_email(session.get('email'))
    if not user:
        flash("User profile not found.", "danger")
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not full_name:
            flash("Full name cannot be empty.", "danger")
            return render_template('profile.html', user=user)
            
        password_hash = None
        # If user wants to change password
        if current_password or new_password or confirm_password:
            if not (current_password and new_password and confirm_password):
                flash("To change password, please fill in current, new, and confirm password fields.", "danger")
                return render_template('profile.html', user=user)
                
            if not check_password_hash(user['password_hash'], current_password):
                flash("Incorrect current password.", "danger")
                return render_template('profile.html', user=user)
                
            if new_password != confirm_password:
                flash("New passwords do not match.", "danger")
                return render_template('profile.html', user=user)
                
            password_hash = generate_password_hash(new_password)
            
        update_user_profile(user['email'], full_name, password_hash)
        
        # Update session name
        session['name'] = full_name
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))
        
    return render_template('profile.html', user=user)

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/admin/data')
@admin_required
def admin_data():
    feedbacks = get_all_feedback()
    users = get_all_users()
    
    # Calculate statistics
    total_feedback = len(feedbacks)
    total_users = len([u for u in users if u['role'] == 'user'])
    
    # Dynamic listing for available options based on DEPT_DOCTORS
    hospitals_list = ["Apollo Hospital", "JSS Hospital", "Manipal Hospital", "Fortis Hospital"]
    doctors_list = [doc for docs in DEPT_DOCTORS.values() for doc in docs]
    
    total_hospitals = len(hospitals_list)
    total_doctors = len(doctors_list)
    
    pos_feedbacks = [f for f in feedbacks if f['predicted_sentiment'].lower() == 'positive']
    neg_feedbacks = [f for f in feedbacks if f['predicted_sentiment'].lower() == 'negative']
    
    total_pos = len(pos_feedbacks)
    total_neg = len(neg_feedbacks)
    
    # Doctor Performance Calculation
    doctor_stats = {}
    for doc in doctors_list:
        doc_feedbacks = [f for f in feedbacks if f['doctor'].lower() == doc.lower()]
        total_doc = len(doc_feedbacks)
        pos_doc = len([f for f in doc_feedbacks if f['predicted_sentiment'].lower() == 'positive'])
        neg_doc = total_doc - pos_doc
        pos_rating = (pos_doc / total_doc * 100) if total_doc > 0 else 0
        doctor_stats[doc] = {
            'total': total_doc,
            'positive': pos_doc,
            'negative': neg_doc,
            'rating': round(pos_rating, 1)
        }
        
    # Hospital Performance Calculation
    hospital_stats = {}
    for hosp in hospitals_list:
        hosp_feedbacks = [f for f in feedbacks if f['hospital'].lower() == hosp.lower()]
        total_hosp = len(hosp_feedbacks)
        pos_hosp = len([f for f in hosp_feedbacks if f['predicted_sentiment'].lower() == 'positive'])
        pos_rating = (pos_hosp / total_hosp * 100) if total_hosp > 0 else 0
        hospital_stats[hosp] = {
            'total': total_hosp,
            'positive': pos_hosp,
            'negative': total_hosp - pos_hosp,
            'rating': round(pos_rating, 1)
        }
        
    # Determine best performing hospital
    best_hosp = "None"
    best_hosp_rating = -1
    for hosp, stats in hospital_stats.items():
        if stats['total'] > 0 and stats['rating'] > best_hosp_rating:
            best_hosp = hosp
            best_hosp_rating = stats['rating']
            
    # Determine best performing doctor
    best_doc = "None"
    best_doc_rating = -1
    for doc, stats in doctor_stats.items():
        if stats['total'] > 0 and stats['rating'] > best_doc_rating:
            best_doc = doc
            best_doc_rating = stats['rating']
            
    # Hospital rankings sorted by rating % descending
    hospital_rankings = [
        {'hospital': k, 'rating': v['rating'], 'total': v['total']} 
        for k, v in hospital_stats.items()
    ]
    hospital_rankings.sort(key=lambda x: (x['rating'], x['total']), reverse=True)
    
    # Doctor rankings sorted by rating % descending
    doctor_rankings = [
        {'doctor': k, 'rating': v['rating'], 'total': v['total']} 
        for k, v in doctor_stats.items()
    ]
    doctor_rankings.sort(key=lambda x: (x['rating'], x['total']), reverse=True)
    
    # Monthly Feedback Trends (last 6 months or simple month aggregation)
    monthly_trends = {}
    for f in feedbacks:
        ts = f.get('timestamp', '')
        if ts:
            try:
                dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                month_name = dt.strftime('%B %Y')
                monthly_trends[month_name] = monthly_trends.get(month_name, 0) + 1
            except:
                pass
                
    # Sort monthly trends chronologically (simple sort on YYYY-MM helper)
    sorted_months = sorted(monthly_trends.keys(), key=lambda x: datetime.strptime(x, '%B %Y'))
    monthly_data = {
        'labels': sorted_months,
        'values': [monthly_trends[m] for m in sorted_months]
    }
    
    # Response JSON payload
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_hospitals': total_hospitals,
            'total_doctors': total_doctors,
            'total_feedback': total_feedback,
            'positive_reviews': total_pos,
            'negative_reviews': total_neg,
            'best_hospital': f"{best_hosp} ({best_hosp_rating}%)" if best_hosp_rating >= 0 else "N/A",
            'best_doctor': f"{best_doc} ({best_doc_rating}%)" if best_doc_rating >= 0 else "N/A"
        },
        'doctor_stats': doctor_stats,
        'hospital_stats': hospital_stats,
        'hospital_rankings': hospital_rankings,
        'doctor_rankings': doctor_rankings,
        'monthly_trends': monthly_data,
        'feedbacks': feedbacks  # Search and filtering will be done on the client-side for speed
    })

if __name__ == '__main__':
    # Listen on localhost:5000
    app.run(debug=True, port=5000)
