from flask import Flask, render_template, request, jsonify
import requests
import os
from config import API_KEY

app = Flask(__name__)

# Azure configuratie
if __name__ == '__main__':
    # Lokale ontwikkeling
    app.run(debug=True)
else:
    # Azure productie
    app.config.update(
        SERVER_NAME=os.environ.get('WEBSITE_HOSTNAME', None),
        SECRET_KEY=os.environ.get('SECRET_KEY', 'development_key')
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/zoek', methods=['POST'])
def zoek():
    kvk_nummer = request.form.get('kvk_nummer')
    bedrijfsnaam = request.form.get('bedrijfsnaam')
    
    url = "https://api.kvk.nl/test/api/v2/zoeken"
    headers = {
        "apikey": API_KEY,
        "Accept": "application/json"
    }
    
    params = {}
    if kvk_nummer:
        params['kvkNummer'] = kvk_nummer
    if bedrijfsnaam:
        params['naam'] = bedrijfsnaam
        
    try:
        response = requests.get(url, headers=headers, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})