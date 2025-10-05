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

def Economic_Condition_Distribution():
    fig = px.pie(df, names="Economic Condition", title="Economic Condition Distribution")
    graph3_html = pio.to_html(fig, full_html=False)
    return graph3_html

def Distribution_By_Weekday():
    fig = px.bar(df, x="Day Of Week", y="Traffic Density", title="Day of Week vs Avg Traffic Density", color="Day Of Week")
    graph4_html = pio.to_html(fig, full_html=False)
    return graph4_html

def Peek_Hour_Analysis():
    fig = px.sunburst(df, path=["Is Peak Hour", "Vehicle Type"], title="Sunburst: Is Peak Hour & Vehicle Type")
    graph5_html = pio.to_html(fig, full_html=False)
    return graph5_html

def Traffic_Density_by_day():
    fig  = px.pie(df, names='Day Of Week', title='Traffic Distribution by Day of the Week')
    graph6_html = pio.to_html(fig, full_html=False)
    return graph6_html

def Speed_Distribution():
    fig = px.histogram(df, x="Speed", nbins=50, title="Speed Distribution")
    graph7_html = pio.to_html(fig, full_html=False)
    return graph7_html

def Speed_vs_Vehicle_Type():
    fig = px.box(df, x="Vehicle Type", y="Speed", title="Speed by Vehicle Type")
    graph8_html = pio.to_html(fig, full_html=False)
    return graph8_html

def Traffic_Density_Distribution():
    fig = px.histogram(df, x="Traffic Density", nbins=50, title="Traffic Density Distribution")
    graph9_html = pio.to_html(fig, full_html=False)
    return graph9_html

def Traffic_Density_by_Weather():
    fig = px.box(df, x="Weather", y="Traffic Density", title="Traffic Density by Weather")
    graph10_html = pio.to_html(fig, full_html=False)
    return graph10_html

def Hours_vs_Speed():
    fig = px.scatter(df.sample(5000), x="Hour Of Day", y="Speed", size="Traffic Density",
                title="Hour vs Speed (Bubble=Traffic Density)")
    graph11_html = pio.to_html(fig, full_html=False)
    return graph11_html

def Traffic_Distribution_by_Day_of_Week():
    fig = px.pie(df, names='Day Of Week', title='Traffic Distribution by Day of the Week')
    graph12_html = pio.to_html(fig, full_html=False)
    return graph12_html

def Hourly_Speed_vs_Energy():
    fig = px.scatter(df.sample(5000), x="Speed", y="Energy Consumption",
                animation_frame="Hour Of Day", animation_group="City",
                size="Traffic Density", color="City",
                title="Animated Scatter: Hourly Speed vs Energy")
    graph13_html = pio.to_html(fig, full_html=False)
    return graph13_html

def City_wise_avg_Speed():
    fig = px.line(df.groupby(["Day Of Week","City"])["Speed"].mean().reset_index(),
            x="Day Of Week", y="Speed", color="City", title="City wise Avg Speed across Days")
    graph14_html = pio.to_html(fig, full_html=False)
    return graph14_html

def Random_Event_by_Weather():
    fig = px.bar(df.groupby("Weather")["Random Event Occurred"].mean().reset_index(),
             x="Weather", y="Random Event Occurred", title="Random Events % by Weather")
    graph15_html = pio.to_html(fig, full_html=False)
    return graph15_html

def Day_vvs_Hours_vs_Traffic_Density():
    fig = px.density_heatmap(df, x="Hour Of Day", y="Day Of Week", z="Traffic Density",
                        title="Day vs Hour vs Traffic Density")
    graph16_html = pio.to_html(fig, full_html=False)
    return graph16_html

def Traffic_Density_Treemap():
    fig = px.treemap(df, path=["City", "Day Of Week"], values="Traffic Density",
                 title="Traffic Density Treemap")
    graph17_html = pio.to_html(fig, full_html=False)
    return graph17_html

def Economic_Condition_Distribution():
    fig = px.sunburst(df, path=["Economic Condition", "Vehicle Type"], title="Sunburst: Economic Condition & Vehicle Type")
    graph18_html = pio.to_html(fig, full_html=False)
    return graph18_html

@app.route('/categorical_analysis')
def categorical_analysis():
    graph1 = Vehicle_Type_Distribution()
    graph2 = Traffic_Condition_Distribution()
    graph3 = Economic_Condition_Distribution()
    graph4 = Distribution_By_Weekday()
    graph5 = Peek_Hour_Analysis()
    return render_template('categorical_analysis.html', graph1_html=graph1, graph2_html=graph2, graph3_html=graph3, graph4_html=graph4, graph5_html=graph5)

@app.route('/numerical_analysis')
def numerical_analysis():
    graph6 = Traffic_Density_by_day()
    graph7 = Speed_Distribution()
    graph8 = Speed_vs_Vehicle_Type()
    graph9 = Traffic_Density_Distribution()
    graph10 = Traffic_Density_by_Weather()
    graph11 = Hours_vs_Speed()
    return render_template('numerical_analysis.html', graph6_html=graph6, graph7_html=graph7, graph8_html=graph8, graph9_html=graph9, graph10_html=graph10, graph11_html=graph11)


@app.route('/mixed_relations')
def mixed_relations():
    graph12 = Traffic_Distribution_by_Day_of_Week()
    graph13 = Hourly_Speed_vs_Energy()
    graph14 = City_wise_avg_Speed()
    graph15 = Random_Event_by_Weather()
    graph16 = Day_vvs_Hours_vs_Traffic_Density()
    graph17 = Traffic_Density_Treemap()
    graph18 = Economic_Condition_Distribution()
    return render_template('mixed_relations.html', graph12_html=graph12, graph13_html=graph13, graph14_html=graph14, graph15_html=graph15, graph16_html=graph16, graph17_html=graph17, graph18_html=graph18)

if __name__ == '__main__':
    if not os.path.exists('users.db'):
        with app.app_context():
            db.create_all()
app.run(debug=True)