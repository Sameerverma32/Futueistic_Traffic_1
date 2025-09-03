from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import joblib

df = pd.read_csv('futuristic_city_traffic_sampled.csv')

#load the saved model and preprocessing components
model = joblib.load('traffic_density_model.pkl')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')



@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/base.html')
def base():
    return render_template('base.html')