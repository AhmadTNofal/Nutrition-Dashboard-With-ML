from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/index.html')
def index():
    # This route will render the index.html template
    return render_template('index.html')

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
    return render_template('graphs.html')

if __name__ == '__main__':
    app.run(debug=True)