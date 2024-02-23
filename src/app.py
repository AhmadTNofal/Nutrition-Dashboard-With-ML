from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    # Render the index.html template with dark mode state
    dark_mode = 'dark' if session.get('dark_mode') else ''
    return render_template('index.html', dark_mode=dark_mode)

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
