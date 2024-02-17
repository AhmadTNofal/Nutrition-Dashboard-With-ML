import csv
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Open and read the CSV file
    with open('data/FeedingDashboardData.csv', 'r') as file:
        reader = csv.reader(file)
        # Convert CSV data to list (or use any suitable data structure)
        csv_data = list(reader)
    
#     # Pass the first row of CSV data (or any specific data you need) to the template
#     return render_template('index.html', csv_text=csv_data[0][0])

if __name__ == "__main__":
    app.run(debug=True)
