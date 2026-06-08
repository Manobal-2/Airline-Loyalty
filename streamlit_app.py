
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title='Airline Loyalty Intelligence',layout='wide')

st.title('Airline Loyalty Behavioral Intelligence System')

loyalty = pd.read_csv('data/Customer Loyalty History.csv')
activity = pd.read_csv('data/Customer Flight Activity.csv')

activity_summary = activity.groupby('Loyalty Number').agg({
    'Total Flights':'sum',
    'Distance':'sum',
    'Points Accumulated':'sum',
    'Points Redeemed':'sum'
}).reset_index()

data = loyalty.merge(activity_summary,on='Loyalty Number',how='left')

data['Cancellation'] = data['Cancellation Year'].notna().astype(int)

st.subheader('Business Overview')

col1,col2,col3 = st.columns(3)

col1.metric('Customers',len(data))
col2.metric('Average CLV',round(data['CLV'].mean(),2))
col3.metric('Churn Rate',str(round(data['Cancellation'].mean()*100,2)) + '%')

fig = px.histogram(data,x='CLV')
st.plotly_chart(fig,use_container_width=True)

st.subheader('Customer Lookup')

customer_id = st.selectbox('Select Customer',data['Loyalty Number'].unique())

customer = data[data['Loyalty Number']==customer_id]

st.dataframe(customer)

st.subheader('Behavioral Insights')

segment_fig = px.scatter(
    data,
    x='Distance',
    y='CLV',
    color='Loyalty Card'
)

st.plotly_chart(segment_fig,use_container_width=True)

st.subheader('Retention Recommendation')

if customer['CLV'].values[0] > data['CLV'].quantile(0.75):
    st.success('Premium retention outreach recommended')
else:
    st.info('Standard engagement campaign recommended')
