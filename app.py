import streamlit as st
import datetime
import pandas as pd
import requests
import numpy as np

'''
# Predict your taxi fare in New York City!
'''

st.markdown('''
Hi dear New-York traveller! 🚕
''')

st.markdown('''
Please be aware that your journey in the Big Apple will be quite expensive, however we will try to help you predict how much broker you will be at the end of your trip! 🤑
''')


'''
### Please enter your ride parameters
'''

st.sidebar.markdown(f"""
    # Le Wagon Taxi Consulting
    """)

gif_key = st.secrets['GIF_TOKEN']

gif_topic = st.text_input('Choose your gif topic!')
if gif_topic:
    response = requests.get(f'https://api.giphy.com/v1/gifs/random?api_key={gif_key}&tag={gif_topic}&rating=g')
    #
    if response.status_code == 200:
        data = response.json()
        gif_url = data['data']['images']['original']['url']
        st.image(gif_url, caption=f"Hello little {gif_topic}!")
    else:
        st.error("Failed to fetch GIF. Please try again.")

d = st.date_input(
    "Date of pickup",
    datetime.date(2019, 7, 6))
t = st.time_input(
    "Time of pickup",
    datetime.time(8, 45))
st.write('Your pickup is on', d, 'at', t)

p_long = st.number_input('Pickup longitude', value=-74.0060, step=0.0001, format="%.4f")
p_lat = st.number_input('Pickup latitude', value = 40.7128, step=0.0001, format="%.4f")
st.write('Your pickup location is at longitude', np.round(p_long,4), 'and latitude', np.round(p_lat,4))

d_long = st.number_input('Dropoff longitude', value=-74.0260,step=0.0001, format="%.4f")
d_lat = st.number_input('Dropoff latitude', value = 40.7328, step=0.0001, format="%.4f")
st.write('Your dropoff location is at longitude', np.round(d_long, 4), 'and latitude', np.round(d_lat,4))

pass_count = st.number_input('Passenger count', min_value=1, max_value=8, value=1, step=1)
st.write('You will be', pass_count, 'passenger(s)')


url = 'https://wagon-data-tpl-image-bqfgf6mkyq-ew.a.run.app/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

params = dict(
        pickup_datetime= f"{d} {t}",
        pickup_longitude= p_long,
        pickup_latitude= p_lat,
        dropoff_longitude= d_long,
        dropoff_latitude= d_lat,
        passenger_count= pass_count,
    )

result = requests.get(url, params=params).json()

st.write('### Here is your fare prediction:',np.round(result['fare'],1),'$')

@st.cache_data
def get_map_data(lat_1, long_1, lat_2, long_2):

    return pd.DataFrame(
            [[lat_1,long_1],[lat_2,long_2]],
            columns=['lat', 'lon']
        )

df = get_map_data(lat_1=p_lat, long_1=p_long, lat_2=d_lat, long_2=d_long)

st.map(data=df)

st.markdown('''
# Have a good trip!
            '''
            )
