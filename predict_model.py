# predict_model.py
import joblib
from alpha_vantage.timeseries import TimeSeries

def get_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data

def prepare_data(data):
    data = data[['1. open', '2. high', '3. low', '4. close', '5. volume']]
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data['Market_High_Indicator'] = (data['High'] > data['Close'].shift(1)).astype(int)
    return data

def predict_next_day(symbol, api_key):
    # Load the trained model
    model = joblib.load('trained_model.pkl')

    # Extract data for the next day from Alpha Vantage API
    df = get_stock_data(symbol, api_key)
    df = prepare_data(df)
    last_row_features = df.drop(columns=['Market_High_Indicator']).iloc[-1]
    last_row_features = last_row_features.values.reshape(1, -1)

    # Predict the next day's market high indicator
    next_day_prediction = model.predict(last_row_features)
    next_day_prediction_binary = 1 if next_day_prediction > 0.5 else 0

    return next_day_prediction_binary

if __name__ == "__main__":
    # Symbol and API key for Alpha Vantage API
    symbol = 'RELIANCE.BSE'
    api_key = 'RDW63LUED9U3S55M'

    # Call the predict_next_day function
    prediction = predict_next_day(symbol, api_key)
    print("Predicted Market High Indicator for the Next Day:", prediction)
