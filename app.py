from flask import Flask, request, jsonify
import pickle
import pandas as pd
from werkzeug.serving import run_simple

# Load the model
with open('loan_prediction_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the training data to get feature columns
X_train = pd.read_csv('lending_club_loan_dataset.csv')  # Make sure this file exists

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Loan Prediction Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input JSON data
        data = request.get_json(force=True)

        # Convert to DataFrame
        input_data = pd.DataFrame(data, index=[0])

        # Ensure all features are present in the input
        missing_cols = set(X_train.columns) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0  # Fill missing columns with 0

        # If your model uses one-hot encoding, you may need to create those features:
        # Example: If 'home_ownership' is a categorical variable that was one-hot encoded
        if 'home_ownership' in input_data.columns:
            input_data = pd.get_dummies(input_data, columns=['home_ownership'], prefix='', prefix_sep='')

        # Reorder columns to match the training set
        input_data = input_data.reindex(columns=X_train.columns, fill_value=0)

        # Make prediction
        prediction = model.predict(input_data)

        # Return the result as JSON
        return jsonify({'predicted_bad_loan': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Return error message with status 400


# Use run_simple for better compatibility in Jupyter
if __name__ == '__main__':
    run_simple('localhost', 5000, app)
