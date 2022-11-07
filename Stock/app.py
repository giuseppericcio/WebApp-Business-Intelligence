import datetime as dt
import plotly_express as px
import streamlit as st
import yfinance as yf
from prophet import Prophet

st.set_page_config(
    page_title = "Stock Prices Companies",
    page_icon = ":moneybag:",
    layout = "wide"
)

st.title(":moneybag: Stock Prices Companies")

#Sidebar
st.sidebar.subheader('Ticker Query')

period_list = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']

with open('ticker.txt','r') as fp:
    ticker_list = fp.read().split('\n')

period_selection = st.sidebar.selectbox(
    label = 'Period',
    options = period_list,
    index = period_list.index('1y')
)

ticker_selection = st.sidebar.selectbox(
    label = 'Ticker Symbol',
    options = ticker_list,
    index = ticker_list.index('AAPL')
)

#Data fetch
ticker_data = yf.Ticker(ticker_selection)

ticker_df = ticker_data.history(period_selection)
ticker_df = ticker_df.rename_axis('Date').reset_index()

ticker_df['Date'] = ticker_df['Date'].dt.date

#Main page
logo_url = ticker_data.info['logo_url']

st.image(logo_url)

company_name = ticker_data.info['longName']
st.header(company_name)

company_info = ticker_data.info['longBusinessSummary']
st.info(company_info)

st.dataframe(ticker_df)

#Model
# y(t) = a*growth(t) + b*season(t)+ c*holiday(t) + e(t)
# g(t) = logistic o linear
# s(t) = additivo o moltiplicativo
# h(t) = periodi di tempo particolari

#Prophet sidebar
st.sidebar.subheader('Prophet Query')

horizon_selection = st.sidebar.slider(
    label = 'Forecasting horizon',
    min_value = 1,
    max_value = 365,
    value = 90
)

growth_selection = st.sidebar.radio(
    label = 'Growth selection',
    options = ['linear', 'logistic']
)

if growth_selection == 'logistic':
    cap = st.sidebar.number_input('Cap', min_value = 0)
    floor = st.sidebar.number_input('Floor', min_value = 0)
    if floor >= cap:
        st.sidebar.error('Cap must be higher than Floor, switching to linear')
        growth_selection = 'linear'

seasonality_selection = st.sidebar.radio(
    label = 'Seasonality type',
    options = ['additive', 'multiplicative']
)

with st.sidebar.expander('Seasonality components:'):
    weekly_selection = st.checkbox('Weekly', value = True)
    monthly_selection = st.checkbox('Monthly')
    yearly_selection = st.checkbox('Yearly', value = True)


with open('holidays.txt','r') as fp:
    holiday_country_list = fp.read().split('\n')
    holiday_country_list.insert(0, 'None')

holiday_country_selection = st.sidebar.selectbox(
    label = 'Holiday Country',
    options = holiday_country_list,
    index = holiday_country_list.index('IT')
)

changepoint_prior_selection = st.sidebar.slider(
    label = 'Changepoint prior scale',
    min_value = 0.01,
    max_value = 0.50,
    value = 0.25
)

#Forecasting
st.subheader ('Forecasting')

with st.spinner('Fitting'):
    prophet_df = ticker_df.rename(columns = {'Date':'ds', 'Close':'y'})
    if growth_selection == 'logistic':
        prophet_df['cap'] = cap
        prophet_df['floor'] = floor
    model = Prophet(
        growth = growth_selection,
        seasonality_mode = seasonality_selection,
        weekly_seasonality = weekly_selection,
        yearly_seasonality = yearly_selection,
        changepoint_prior_scale = changepoint_prior_selection
    )
    if monthly_selection:
        model.add_seasonality('Monthly', period = 30.5, fourier_order = 5)
    if holiday_country_selection != 'None':
        model.add_country_holidays(holiday_country_selection)
    model.fit(prophet_df)

with st.spinner('Predizione'):
    future = model.make_future_dataframe(horizon_selection, freq = 'D')
    if growth_selection == 'logistic':
        future['cap'] = cap
        future['floor'] = floor
    forecast = model.predict(future)

st.dataframe(forecast)

fig = px.scatter(prophet_df, x='ds', y='y', labels = {'ds':'Day', 'y':'Close'})
fig.add_scatter(x=forecast['ds'], y = forecast['yhat'], name = 'yhat')
fig.add_scatter(x=forecast['ds'], y = forecast['yhat_lower'], name = 'yhat_lower')
fig.add_scatter(x=forecast['ds'], y = forecast['yhat_upper'], name = 'yhat_upper')

st.plotly_chart(fig)