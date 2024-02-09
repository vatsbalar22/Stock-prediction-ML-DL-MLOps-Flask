# train_model.py

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from alpha_vantage.timeseries import TimeSeries
import joblib

def get_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data

def train_model(symbol, api_key):
    # Extract data from Alpha Vantage API
    df = get_stock_data(symbol, api_key)

    # Prepare data
    df = prepare_data(df)

    # Split the data into features (X) and target (y)
    X = df.drop(columns=['Market_High_Indicator'])
    y = df['Market_High_Indicator']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Save the trained model
    joblib.dump(model, 'trained_model.pkl')

def prepare_data(data):
    data = data[['1. open', '2. high', '3. low', '4. close', '5. volume']]
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data['Market_High_Indicator'] = (data['High'] > data['Close'].shift(1)).astype(int)
    return data

if __name__ == "__main__":
    # Symbol and API key for Alpha Vantage API
    symbol = 'RELIANCE.BSE'
    api_key = 'RDW63LUED9U3S55M'

    # Call the train_model function
    train_model(symbol, api_key)
