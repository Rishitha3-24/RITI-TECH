from flask import Flask, redirect, url_for, render_template, request, Response
import json

app = Flask(__name__)

arr = []

@app.route('/')
def redirect_to_home():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        data = request.form['input']
        arr.append(data)
        return redirect(url_for('home'))

    elif request.method == 'GET':
        response_data = {
            "value": arr
        }
        return Response(json.dumps(response_data), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
