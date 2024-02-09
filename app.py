# app.py

from flask import Flask, render_template, request
from predict_model import predict_next_day

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symbol = request.form['symbol']
    api_key = request.form['api_key']
    
    prediction = predict_next_day(symbol, api_key)
    
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
