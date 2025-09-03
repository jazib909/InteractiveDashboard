# 📊 Interactive Data Visualization Dashboard

A beautiful, real-time data visualization dashboard built with Python Flask that displays live stock prices, cryptocurrency data, and weather information with interactive charts and modern UI.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3+-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **📈 Real-time Stock Market Data**: Live tracking of AAPL, GOOGL, MSFT, AMZN, TSLA
- **₿ Cryptocurrency Monitoring**: Real-time prices for Bitcoin, Ethereum, and Cardano  
- **🌤️ Global Weather Data**: Weather conditions for major cities worldwide
- **📊 Interactive Charts**: Beautiful charts with Chart.js and Plotly integration
- **🔄 WebSocket Updates**: Real-time data streaming every 2 seconds
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🎨 Modern UI**: Dark theme with glassmorphism effects and smooth animations
- **⚡ Live Connection Status**: Visual indicators for connection health

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd jazib
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000` to view the dashboard

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for Python
- **Flask-SocketIO**: WebSocket support for real-time updates
- **yfinance**: Yahoo Finance API for stock and crypto data
- **Plotly**: Interactive plotting library
- **Pandas & NumPy**: Data manipulation and analysis

### Frontend
- **HTML5 & CSS3**: Modern web standards with CSS Grid and Flexbox
- **Bootstrap 5**: Responsive framework
- **Chart.js**: Interactive charts and visualizations
- **Socket.IO**: Real-time bidirectional communication
- **Font Awesome**: Icon library
- **Google Fonts**: Inter font family for modern typography

## 📊 Dashboard Components

### 1. Stock Market Section
- Real-time price tracking for major stocks
- Price change indicators with color coding
- Percentage change calculations
- Interactive line charts

### 2. Cryptocurrency Section  
- Bitcoin, Ethereum, and Cardano price monitoring
- Higher volatility simulation for crypto markets
- Real-time price movements
- Dedicated crypto charts

### 3. Weather Data Section
- Mock weather data for 5 major cities
- Temperature, humidity, and pressure readings
- Realistic weather pattern simulation
- Beautiful weather cards with icons

### 4. Interactive Charts
- Real-time updating line charts
- Multiple datasets on single charts
- Smooth animations and transitions
- Color-coded data series

## 🔧 Configuration

### Data Update Frequency
The dashboard updates every 2 seconds by default. You can modify this in `app.py`:

```python
time.sleep(2)  # Change this value to adjust update frequency
```

### Adding New Stocks
To track additional stocks, modify the symbols list in `app.py`:

```python
self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA']  # Add new symbols
```

### Adding New Cryptocurrencies
Add new crypto symbols to track:

```python
self.crypto_symbols = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD']  # Add new cryptos
```

## 🎨 UI Customization

### Color Scheme
The dashboard uses CSS custom properties for easy theming. Modify the colors in `templates/index.html`:

```css
:root {
    --primary-color: #00d4ff;     /* Main accent color */
    --secondary-color: #ff6b6b;   /* Secondary accent */
    --success-color: #51cf66;     /* Success/positive */
    --warning-color: #ffd43b;     /* Warning/neutral */
    --danger-color: #ff6b6b;      /* Danger/negative */
    --dark-bg: #0a0a0a;           /* Main background */
    --card-bg: #1a1a1a;           /* Card background */
}
```

### Chart Colors
Customize chart colors by modifying the `getChartColor()` function:

```javascript
const colors = [
    '#00d4ff', '#ff6b6b', '#51cf66', '#ffd43b', '#ff8cc8',
    '#845ef7', '#ffa94d', '#69db7c', '#74c0fc', '#fa5252'
];
```

## 📱 Responsive Design

The dashboard is fully responsive and works on:
- 🖥️ Desktop computers (1200px+)
- 💻 Laptops (992px - 1199px)
- 📱 Tablets (768px - 991px)
- 📱 Mobile phones (320px - 767px)

## 🔄 Real-time Features

### WebSocket Connection
- Automatic reconnection on connection loss
- Visual connection status indicator
- Real-time data streaming
- Error handling and fallback mechanisms

### Data Generation
- Realistic stock price movements (±2% volatility)
- Higher crypto volatility (±5%)
- Weather pattern simulation
- Timestamp tracking for all data points

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:

1. **Gunicorn** for production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn --worker-class eventlet -w 1 app:app
   ```

2. **Environment Variables** for configuration:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   ```

3. **Nginx** for reverse proxy and static file serving

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Change port in app.py
   socketio.run(app, debug=True, host='0.0.0.0', port=5001)
   ```

2. **Missing dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **WebSocket connection issues**
   - Check firewall settings
   - Ensure no VPN interference
   - Try different browser

### Debug Mode
Enable debug mode for development:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

## 📈 Performance Optimization

- Data points are limited to last 50 entries per symbol
- Charts update with minimal animation for smooth performance
- WebSocket events are batched for efficiency
- CSS animations use GPU acceleration

## 🤝 Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the console logs in your browser
3. Check the terminal output where the Flask app is running

## 🎉 Acknowledgments

- Yahoo Finance for providing financial data APIs
- Chart.js and Plotly for excellent charting libraries
- Bootstrap team for the responsive framework
- Font Awesome for beautiful icons

---

**Enjoy exploring your real-time data dashboard! 📊✨**
