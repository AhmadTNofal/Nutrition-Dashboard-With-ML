import csv
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
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
    df = pd.read_csv('data\\FeedingDashboardData.csv')

    # Assuming 'encounterId' is the first column and 'referral' is the last
    features_columns = df.columns[1:-1] 

    # Threshold for minimum number of non-missing features to attempt a prediction
    min_features_threshold = 5  # Example threshold, adjust based on your criteria

    # Flag rows with insufficient data
    df['sufficient_data'] = df[features_columns].notnull().sum(axis=1) >= min_features_threshold

    # Split the DataFrame based on data sufficiency
    df_sufficient_data = df[df['sufficient_data']].copy()
    df_insufficient_data = df[~df['sufficient_data']].copy()

    # Process rows with sufficient data for prediction
    encounter_ids_sufficient = df_sufficient_data['encounterId']
    X_sufficient = df_sufficient_data[features_columns]
    y_sufficient = df_sufficient_data['referral']

    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X_sufficient)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        X_scaled, y_sufficient, encounter_ids_sufficient, test_size=0.2, random_state=42
    )

    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]
    referral_needed = probabilities > 0.5

    # Prepare results for clients with sufficient data
    results = [{
        'patient_number': i + 1,
        'encounter_id': int(encounter_id),
        'referral_probability': f"{prob:.2f}",
        'needs_referral': "Yes" if need else "No",
        'color': "red" if need else "green"
    } for i, (encounter_id, prob, need) in enumerate(zip(ids_test, probabilities * 100, referral_needed))]

    # Add clients with insufficient data to results
    for row in df_insufficient_data.itertuples():
        results.append({
            'patient_number': len(results) + 1,
            'encounter_id': row.encounterId,
            'referral_probability': "Missing Data",
            'needs_referral': "N/A",
            'color': "yellow"
        })

    referrals = sum(res['needs_referral'] == "Yes" for res in results if res['needs_referral'] != "N/A")
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
    df = pd.read_csv('data\FeedingDashboardData.csv')

    # Impute missing values with the mean
    imputer = SimpleImputer(strategy='mean')
    df.iloc[:, 1:-1] = imputer.fit_transform(df.iloc[:, 1:-1])

    scaler = StandardScaler()
    df.iloc[:, 1:-1] = scaler.fit_transform(df.iloc[:, 1:-1])

    X = df.drop(['encounterId', 'referral'], axis=1)
    y = df['referral']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    svc = SVC(kernel='rbf', probability=True, random_state=42) 
    svc.fit(X_train, y_train)

    probabilities = svc.predict_proba(X_test)[:, 1]

    threshold = 0.5
    referral_needed = probabilities > threshold
    
    #count the number of referrals needed
    referrals = sum(referral_needed)

    #count the sum of dont need refferal
    count_no_referral = len(referral_needed) - referrals

    #today's date
    Today = date.today().strftime("%B %d, %Y")

    # Store results in a list of dictionaries
    results = [{'patient_number': i+1, 
                'referral_probability': f"{prob:.2f}", 
                'needs_referral': "Yes" if need else "No",
                'color': "red" if need else "green"} 
            for i, (prob, need) in enumerate(zip(probabilities*100, referral_needed))]

    # Render the graphs.html template with dark mode state
    dark_mode = 'dark' if session.get('dark_mode') else ''
    return render_template('graphs.html',results=results,count = referrals,sum = count_no_referral+referrals,today = Today, dark_mode=dark_mode)

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
