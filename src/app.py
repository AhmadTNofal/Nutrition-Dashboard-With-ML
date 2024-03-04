import csv
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import json
from datetime import date

app = Flask(__name__)

def get_data_by_encounter_id(encounter_id):
    data = []
    with open('data\FeedingDashboardData.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['encounterId'] == encounter_id:
                data.append(row)
                break  # Assuming encounter_id is unique, break after finding the match
    return data

@app.route('/')

@app.route('/index.html')
def index():
    # Load data
    df = pd.read_csv("data/FeedingDashboardData.csv")

    # Columns for the new algorithm
    X = df[['feed_vol', 'oxygen_flow_rate', 'resp_rate', 'bmi']]
    y = df['referral']

    # Pipeline for imputation, normalization, and model training
    pipeline = make_pipeline(
        SimpleImputer(strategy='median'),
        StandardScaler(),
        SVC(probability=True, random_state=42)
    )

    # Train model on the entire dataset
    pipeline.fit(X, y)

    # Predict and calculate confidence scores
    predicted_referrals = pipeline.predict(X)
    probabilities = pipeline.predict_proba(X)
    confidence_scores = probabilities.max(axis=1) * 100

    # Prepare output
    results = [{
        'patient_number': i + 1,
        'encounter_id': int(row['encounterId']),
        'referral_probability': f"{conf_score:.2f}",
        'needs_referral': "Yes" if pred_referral else "No",
        'color': "red" if pred_referral else "green"
    } for i, (row, pred_referral, conf_score) in enumerate(zip(df.to_dict('records'), predicted_referrals, confidence_scores))]

    referrals = sum(res['needs_referral'] == "Yes" for res in results)
    count_no_referral = len(results) - referrals
    Today = date.today().strftime("%B %d, %Y")
    dark_mode = 'dark' if session.get('dark_mode') else ''

    # Render the HTML template with the results
    return render_template('index.html', results=results, count=referrals, sum=len(results), today=Today, dark_mode=dark_mode)

@app.route('/toggle-dark-mode', methods=['POST'])
def toggle_dark_mode():
    # Toggle the dark mode state in the session
    session['dark_mode'] = not session.get('dark_mode', False)
    # Return a 204 no content response, as we only need to toggle the state
    return ('', 204)

@app.route('/index', methods=['POST'])
def upload_file():
    # This route will handle the file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # save and process files
            pass
    return redirect(url_for('index'))

@app.route('/graphs.html')
def graphs():
    # Load data
    df = pd.read_csv("data/FeedingDashboardData.csv")

    # Columns for the new algorithm
    X = df[['feed_vol', 'oxygen_flow_rate', 'resp_rate', 'bmi']]
    y = df['referral']

    # Pipeline for imputation, normalization, and model training
    pipeline = make_pipeline(
        SimpleImputer(strategy='median'),
        StandardScaler(),
        SVC(probability=True, random_state=42)
    )

    # Train model on the entire dataset
    pipeline.fit(X, y)

    # Predict and calculate confidence scores
    predicted_referrals = pipeline.predict(X)
    probabilities = pipeline.predict_proba(X)
    confidence_scores = probabilities.max(axis=1) * 100

    # Prepare output
    results = [{
        'patient_number': i + 1,
        'encounter_id': int(row['encounterId']),
        'referral_probability': f"{conf_score:.2f}",
        'needs_referral': "Yes" if pred_referral else "No",
        'color': "red" if pred_referral else "green"
    } for i, (row, pred_referral, conf_score) in enumerate(zip(df.to_dict('records'), predicted_referrals, confidence_scores))]

    referrals = sum(res['needs_referral'] == "Yes" for res in results)
    count_no_referral = len(results) - referrals
    Today = date.today().strftime("%B %d, %Y")
    dark_mode = 'dark' if session.get('dark_mode') else ''

        # Prepare data for pie chart
    needs_referral_count = sum(predicted_referrals)
    no_referral_count = len(predicted_referrals) - needs_referral_count
    pie_data = [needs_referral_count, no_referral_count]

    # Prepare data for histogram
    histogram_data = list(confidence_scores)

    # Convert data to JSON for JavaScript
    pie_data_json = json.dumps(pie_data)
    histogram_data_json = json.dumps(histogram_data)

    # Render the HTML template with the results
    return render_template('graphs.html', results=results, count=referrals, sum=len(results), today=Today, dark_mode=dark_mode, pie_data=pie_data_json, histogram_data=histogram_data_json,)

@app.route('/data.html')
def data():
    #today's date
    Today = date.today().strftime("%B %d, %Y")
    encounter_id = request.args.get('encounterId')
    data = get_data_by_encounter_id(encounter_id)
    dark_mode = 'dark' if session.get('dark_mode') else ''
    return render_template('data.html', today = Today, data=data, dark_mode=dark_mode)

if __name__ == '__main__':
    app.run(debug=True)
