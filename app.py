from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import bcrypt


app = Flask(__name__)
app.config['SECRET KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    password = db.Column(db.String(150), nullable=False)

df = pd.read_csv('futuristic_city_traffic_sampled.csv')

#load the saved model and preprocessing components
model = joblib.load('Analysis/traffic_model.pkl')
scaler = joblib.load('Analysis/scaler.pkl')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter((User.username==username)|(User.email==email)).first()
        if existing_user:
            flash('Username or email already exists')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email_or_username).first() or User.query.filter_by(username=email_or_username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/base')
def base():
    return render_template('base.html')

def Vehicle_Type_Distribution():
    fig = px.pie(df, names="Vehicle Type", title="Vehicle Type Distribution")  
    graph1_html = pio.to_html(fig, full_html=False)
    return graph1_html

def Traffic_Condition_Distribution():
    fig = px.treemap(df, path=["City","Vehicle Type"], title="Treemap: City & Vehicle Type Share")
    graph2_html = pio.to_html(fig, full_html=False)
    return graph2_html

@app.route('/categorical_analysis')
def categorical_analysis():
    graph1 = Vehicle_Type_Distribution()
    return render_template('categorical_analysis.html', graph1_html=graph1)

@app.route('/categorical_analysis')








if __name__ == '__main__':
    if not os.path.exists('users.db'):
        with app.app_context():
            db.create_all()
app.run(debug=True)