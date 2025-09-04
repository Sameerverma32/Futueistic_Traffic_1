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

df = pd.read_csv('futuristic_city_traffic_sampled.csv')

#load the saved model and preprocessing components
model = joblib.load('Analysis/traffic_model.pkl')
scaler = joblib.load('Analysis/scaler.pkl')

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
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

app.run(debug=True)