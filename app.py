from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import joblib
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Load the model and scaler
model_path = os.path.join('model', 'linear_model.pkl')
scaler_path = os.path.join('model', 'scaler.pkl')

try:
    loaded_model = joblib.load(model_path)
    
    loaded_scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    loaded_model = None
    loaded_scaler = None

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/predict', methods=['POST'])
def predict():
    if not loaded_model or not loaded_scaler:
        return jsonify({'error': 'Model or scaler not loaded properly'}), 500
        
    try:
        data = request.json
        
        # Extract features
        square_footage = data['square_footage']
        num_bedrooms = data['num_bedrooms']
        num_bathrooms = data['num_bathrooms']
        zip_code = data['zip_code']
        year_built = data['year_built']
        garage_size = data['garage_size']
        city = data['city']
        nearby_amenities = data['nearby_amenities']
        condition = data['condition']
        crime_rate = data['crime_rate']
        school_rating = data['school_rating']
        
        # Create binary variables for categorical features
        city_dallas = 1 if city == 'Dallas' else 0
        city_houston = 1 if city == 'Houston' else 0
        city_san_antonio = 1 if city == 'San Antonio' else 0
        
        # Amenities encoding
        amenities_park = 1 if 'Park' in nearby_amenities else 0
        amenities_grocery = 1 if 'Grocery' in nearby_amenities else 0
        amenities_gym = 1 if 'Gym' in nearby_amenities else 0
        
        # Condition encoding
        condition_excellent = 1 if condition == 'Excellent' else 0
        condition_good = 1 if condition == 'Good' else 0
        condition_fair = 1 if condition == 'Fair' else 0
        
        # Create input array
        input_data = np.array([[
            square_footage,
            num_bedrooms,
            num_bathrooms,
            zip_code,
            year_built,
            garage_size,
            crime_rate,
            school_rating,
            city_dallas,
            city_houston,
            city_san_antonio,
            amenities_park,
            amenities_grocery,
            amenities_gym,
            condition_excellent,
            condition_good
        ]])
        
        # Scale the input data
        input_data_scaled = loaded_scaler.transform(input_data)
        
        # Make prediction
        prediction = loaded_model.predict(input_data_scaled)
        
        return jsonify({
            'price': float(prediction[0])
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
