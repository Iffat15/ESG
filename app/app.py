from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = 'C:/Users/Anas/Downloads/ESG - Copy/data/energy_data.csv'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE).tail(10)  # Show last 10 entries
        return data.to_json(orient='records')
    return jsonify({"error": "No data available"})

if __name__ == '__main__':
    app.run(debug=True)
