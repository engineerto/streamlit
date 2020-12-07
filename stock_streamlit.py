import streamlit as st
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import datetime
#from colab_everything import ColabStreamlit
#ColabStreamlit('stock_streamlit.py')

st.title('Stock Market Live')

start_date = '2010-01-01' # You can modify the start date!
now = datetime.datetime.now() # The date of today
end_date = now.strftime('%Y-%m-%d') # Transform to this format

stock_name = {'Nvidia': 'NVDA', 'Tesla': 'TSLA', 'Samsung': '005930.ks', 'Kakao': '035720.ks'}

sb_selectbox_country = st.sidebar.selectbox(
    "Select the country", ("US", "Korea")
)

@st.cache
def load_data(stock, source):
    stock_data = data.DataReader(stock, source, start_date, end_date)
    return stock_data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load stock data which is selected
# Load data into the dataframe.
if sb_selectbox_country is "US":
    currency = 'Currency in USD'
    sb_selectbox_stock = st.sidebar.selectbox(
        "Select the stock", ("Nvidia", "Tesla")
    )
    stock_data = load_data(stock_name[sb_selectbox_stock], 'yahoo')

else:
    currency = 'Currency in KRW'
    sb_selectbox_stock = st.sidebar.selectbox(
        "Select the stock", ("Samsung", "Kakao")
    )
    stock_data = load_data(stock_name[sb_selectbox_stock], 'yahoo')

# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show table'):
    st.subheader(sb_selectbox_stock)
    st.write(stock_data)

st.subheader(sb_selectbox_stock)
st.line_chart(stock_data['Close'])

# Choose the date
selected_start_date = st.text_input('Input the start date. e.g. 2019-01-01')
selected_end_date = st.text_input('Input the end date. e.g. 2020-01-01')

# Plot the certain period data
if selected_start_date and selected_end_date:
    filtered_stock_data = stock_data['Close'][selected_start_date:selected_end_date]
    st.subheader(f'{sb_selectbox_stock} from {selected_start_date} to {selected_end_date}')
    fig = plt.figure(figsize=(16, 10))
    filtered_stock_data.plot(grid=True, colormap='coolwarm')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=14)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel(currency, fontsize=20)
    st.write(fig)
