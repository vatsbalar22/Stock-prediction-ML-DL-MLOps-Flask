import streamlit as st
import yfinance as yf
from datetime import datetime
import ta
import plotly.express as px

st.title('Stock Analysis and RSI Scanner Dashboard')

# Sidebar inputs: Symbol, start date, RSI timeframe, and RSI thresholds
symbol = st.sidebar.text_input('Symbol', value='AAPL').upper()
start_date = st.sidebar.date_input('Start date')
rsi_timeframe = st.sidebar.selectbox('RSI Timeframe', ['Daily', 'Weekly', 'Monthly'])
buy_threshold = st.sidebar.number_input('Buy Signal RSI Threshold', min_value=0, max_value=100, value=30)
sell_threshold = st.sidebar.number_input('Sell Signal RSI Threshold', max_value=100, min_value=0, value=70)

# Automatically set end date to today's date
end_date = datetime.today().strftime('%Y-%m-%d')

if symbol:
    data = yf.download(symbol, start=start_date, end=end_date)
    
    if not data.empty:
        # Resample data for the selected RSI timeframe
        if rsi_timeframe == 'Weekly':
            data = data.resample('W').agg({'Open': 'first', 
                                           'High': 'max', 
                                           'Low': 'min', 
                                           'Close': 'last', 
                                           'Adj Close': 'last', 
                                           'Volume': 'sum'})
        elif rsi_timeframe == 'Monthly':
            data = data.resample('M').agg({'Open': 'first', 
                                           'High': 'max', 
                                           'Low': 'min', 
                                           'Close': 'last', 
                                           'Adj Close': 'last', 
                                           'Volume': 'sum'})

        # Calculate RSI
        data['RSI'] = ta.momentum.rsi(data['Adj Close'], window=14)

        # Plotting Adjusted Close Price and RSI
        fig_price = px.line(data, x=data.index, y='Adj Close', title=f'{symbol} Adjusted Close Price')
        fig_rsi = px.line(data, x=data.index, y='RSI', title=f'{symbol} RSI ({rsi_timeframe})')
        fig_rsi.add_hline(y=buy_threshold, line_dash="dot", annotation_text="Buy Threshold", annotation_position="bottom right")
        fig_rsi.add_hline(y=sell_threshold, line_dash="dot", annotation_text="Sell Threshold", annotation_position="top right")

        st.plotly_chart(fig_price)
        st.plotly_chart(fig_rsi)

        # Scanner for Buy and Sell signals
        buy_signals = data[data['RSI'] < buy_threshold]
        sell_signals = data[data['RSI'] > sell_threshold]

        st.subheader('RSI Buy Signals')
        st.write(buy_signals[['Adj Close', 'RSI']])

        st.subheader('RSI Sell Signals')
        st.write(sell_signals[['Adj Close', 'RSI']])
        
        # Option to download data as CSV
        @st.cache
        def convert_df_to_csv(df):
            return df.to_csv().encode('utf-8')

        csv = convert_df_to_csv(data)
        st.download_button("Download data as CSV", csv, f"{symbol}_stock_data.csv", "text/csv", key='download-csv')
    else:
        st.error("No data found for the given dates. Please select a different date range or check the stock symbol.")
else:
    st.info("Please enter a stock symbol to get started.")
