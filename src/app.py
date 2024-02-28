from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
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

    # Store results in a list of dictionaries
    results = [{'patient_number': i+1, 
                'referral_probability': f"{prob:.2f}", 
                'needs_referral': "Yes" if need else "No",
                'color': "red" if need else "green"} 
            for i, (prob, need) in enumerate(zip(probabilities*100, referral_needed))]

    dark_mode = 'dark' if session.get('dark_mode') else ''
    # Pass the results to the template
    return render_template('index.html', results=results,count = referrals,sum = count_no_referral+referrals, dark_mode=dark_mode)


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
    # Render the graphs.html template with dark mode state
    dark_mode = 'dark' if session.get('dark_mode') else ''
    return render_template('graphs.html', dark_mode=dark_mode)

if __name__ == '__main__':
    app.run(debug=True)
