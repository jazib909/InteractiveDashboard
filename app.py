#!/usr/bin/env python3
"""
Interactive Data Visualization Dashboard
A real-time dashboard showcasing stock prices, weather data, and cryptocurrency trends
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import plotly.graph_objs as go
import plotly.utils
import pandas as pd
import numpy as np
import json
import random
import threading
import time
from datetime import datetime, timedelta
import requests
import yfinance as yf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global data storage
stock_data = {}
weather_data = {}
crypto_data = {}

class DataGenerator:
    """Generate and manage real-time data for the dashboard"""
    
    def __init__(self):
        self.is_running = False
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        self.crypto_symbols = ['BTC-USD', 'ETH-USD', 'ADA-USD']
        
    def generate_stock_data(self):
        """Generate realistic stock price movements"""
        global stock_data
        
        for symbol in self.symbols:
            if symbol not in stock_data:
                # Initialize with real data
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d", interval="1m")
                    if not hist.empty:
                        current_price = float(hist['Close'].iloc[-1])
                    else:
                        current_price = 150.0  # fallback
                except:
                    current_price = 150.0  # fallback
                    
                stock_data[symbol] = {
                    'prices': [current_price],
                    'timestamps': [datetime.now()],
                    'current_price': current_price
                }
            
            # Generate next price with some volatility
            current = stock_data[symbol]['current_price']
            change_percent = random.uniform(-0.02, 0.02)  # ±2% max change
            new_price = current * (1 + change_percent)
            
            stock_data[symbol]['prices'].append(new_price)
            stock_data[symbol]['timestamps'].append(datetime.now())
            stock_data[symbol]['current_price'] = new_price
            
            # Keep only last 50 data points
            if len(stock_data[symbol]['prices']) > 50:
                stock_data[symbol]['prices'] = stock_data[symbol]['prices'][-50:]
                stock_data[symbol]['timestamps'] = stock_data[symbol]['timestamps'][-50:]
    
    def generate_crypto_data(self):
        """Generate cryptocurrency price movements"""
        global crypto_data
        
        for symbol in self.crypto_symbols:
            if symbol not in crypto_data:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d", interval="1m")
                    if not hist.empty:
                        current_price = float(hist['Close'].iloc[-1])
                    else:
                        current_price = 45000.0 if 'BTC' in symbol else 3000.0
                except:
                    current_price = 45000.0 if 'BTC' in symbol else 3000.0
                    
                crypto_data[symbol] = {
                    'prices': [current_price],
                    'timestamps': [datetime.now()],
                    'current_price': current_price
                }
            
            # Crypto is more volatile
            current = crypto_data[symbol]['current_price']
            change_percent = random.uniform(-0.05, 0.05)  # ±5% max change
            new_price = current * (1 + change_percent)
            
            crypto_data[symbol]['prices'].append(new_price)
            crypto_data[symbol]['timestamps'].append(datetime.now())
            crypto_data[symbol]['current_price'] = new_price
            
            # Keep only last 50 data points
            if len(crypto_data[symbol]['prices']) > 50:
                crypto_data[symbol]['prices'] = crypto_data[symbol]['prices'][-50:]
                crypto_data[symbol]['timestamps'] = crypto_data[symbol]['timestamps'][-50:]
    
    def generate_weather_data(self):
        """Generate mock weather data for multiple cities"""
        global weather_data
        
        cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Mumbai']
        
        for city in cities:
            if city not in weather_data:
                weather_data[city] = {
                    'temperature': random.uniform(15, 30),
                    'humidity': random.uniform(40, 80),
                    'pressure': random.uniform(980, 1020),
                    'timestamps': [datetime.now()]
                }
            else:
                # Generate realistic weather changes
                temp_change = random.uniform(-1, 1)
                humidity_change = random.uniform(-5, 5)
                pressure_change = random.uniform(-2, 2)
                
                weather_data[city]['temperature'] += temp_change
                weather_data[city]['humidity'] += humidity_change
                weather_data[city]['pressure'] += pressure_change
                
                # Keep within realistic bounds
                weather_data[city]['temperature'] = max(0, min(45, weather_data[city]['temperature']))
                weather_data[city]['humidity'] = max(20, min(100, weather_data[city]['humidity']))
                weather_data[city]['pressure'] = max(950, min(1050, weather_data[city]['pressure']))
                
                weather_data[city]['timestamps'].append(datetime.now())
    
    def run_data_generation(self):
        """Main loop for data generation"""
        self.is_running = True
        while self.is_running:
            try:
                self.generate_stock_data()
                self.generate_crypto_data()
                self.generate_weather_data()
                
                # Emit data to all connected clients
                socketio.emit('data_update', {
                    'stocks': self.format_stock_data(),
                    'crypto': self.format_crypto_data(),
                    'weather': self.format_weather_data()
                })
                
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Error in data generation: {e}")
                time.sleep(5)
    
    def format_stock_data(self):
        """Format stock data for frontend"""
        formatted = {}
        for symbol, data in stock_data.items():
            formatted[symbol] = {
                'current_price': round(data['current_price'], 2),
                'change': round(data['current_price'] - data['prices'][0], 2) if len(data['prices']) > 1 else 0,
                'change_percent': round(((data['current_price'] - data['prices'][0]) / data['prices'][0]) * 100, 2) if len(data['prices']) > 1 else 0,
                'prices': [round(p, 2) for p in data['prices']],
                'timestamps': [t.strftime('%H:%M:%S') for t in data['timestamps']]
            }
        return formatted
    
    def format_crypto_data(self):
        """Format crypto data for frontend"""
        formatted = {}
        for symbol, data in crypto_data.items():
            formatted[symbol] = {
                'current_price': round(data['current_price'], 2),
                'change': round(data['current_price'] - data['prices'][0], 2) if len(data['prices']) > 1 else 0,
                'change_percent': round(((data['current_price'] - data['prices'][0]) / data['prices'][0]) * 100, 2) if len(data['prices']) > 1 else 0,
                'prices': [round(p, 2) for p in data['prices']],
                'timestamps': [t.strftime('%H:%M:%S') for t in data['timestamps']]
            }
        return formatted
    
    def format_weather_data(self):
        """Format weather data for frontend"""
        return {city: {
            'temperature': round(data['temperature'], 1),
            'humidity': round(data['humidity'], 1),
            'pressure': round(data['pressure'], 1)
        } for city, data in weather_data.items()}
    
    def stop(self):
        """Stop data generation"""
        self.is_running = False

# Initialize data generator
data_generator = DataGenerator()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/initial-data')
def get_initial_data():
    """Get initial data for dashboard"""
    return jsonify({
        'stocks': data_generator.format_stock_data(),
        'crypto': data_generator.format_crypto_data(),
        'weather': data_generator.format_weather_data()
    })

@app.route('/api/stock-chart/<symbol>')
def get_stock_chart(symbol):
    """Generate Plotly chart for specific stock"""
    if symbol not in stock_data:
        return jsonify({'error': 'Symbol not found'}), 404
    
    data = stock_data[symbol]
    
    trace = go.Scatter(
        x=data['timestamps'],
        y=data['prices'],
        mode='lines+markers',
        name=symbol,
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff')
    )
    
    layout = go.Layout(
        title=f'{symbol} Price Movement',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Price ($)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'data': 'Connected to dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_data')
def handle_data_request():
    """Handle data request from client"""
    emit('data_update', {
        'stocks': data_generator.format_stock_data(),
        'crypto': data_generator.format_crypto_data(),
        'weather': data_generator.format_weather_data()
    })

def start_data_generation():
    """Start background data generation"""
    thread = threading.Thread(target=data_generator.run_data_generation)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    # Start data generation in background
    start_data_generation()
    
    # Run the Flask-SocketIO app
    print("🚀 Starting Interactive Data Visualization Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("💡 Features: Real-time stocks, crypto prices, and weather data")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
