import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('Visualized Stock Price')

st.sidebar.write("""
# GAFA + Other
This is an application that shows the stock prices. You can select days displayed.
""")

st.sidebar.write("""
## Days displayed
""")

days = st.sidebar.slider('Day', 1, 3650, 365)

st.write(f"""
###  The stock prices of GAFA and a few company in the past **{days}** days. 
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## The Range of Price
    """)
    ymin, ymax = st.sidebar.slider(
        'Select Range',
        0.0, 750.0, (0.0, 500.0)
    )

    tickers = {
        'Apple': 'AAPL',
        'Meta': 'META',
        'Google': 'GOOGL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Amazon': 'AMZN'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        'Select Company',
        list(df.index),
        ['Google', 'Amazon', 'Meta', 'Apple']
    )

    if not companies:
        st.error('Select at least one company')
    else:
        data = df.loc[companies]
        st.write("### Stock Price(USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "Oops! Something Wrong!"
    )