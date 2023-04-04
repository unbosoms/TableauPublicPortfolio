import streamlit as st
import pandas as pd
import json
import requests
from streamlit_elements import nivo 

########################
# Settings
########################

NUM_COLS = 5

st.set_page_config(layout="wide")

PROFILE = 'yuta1985'

if 'mom_limit' not in st.session_state:
    st.session_state.mom_limit=5
if 'wow_limit' not in st.session_state:
    st.session_state.wow_limit=5
if 'otr_limit' not in st.session_state:
    st.session_state.otr_limit=5
if 'ser_limit' not in st.session_state:
    st.session_state.ser_limit=5


# get tableau public data
@st.cache_data
def get_data():

    start = 0
    count = 50 # the number of get count is limited to 50
    data = []
    while(True):
        url = f'https://public.tableau.com/public/apis/workbooks?profileName={PROFILE}&start={start}&count={count}&visibility=NON_HIDDEN'
        res = requests.get(url)
        json = res.json()
        start = json["next"]
        data += json["contents"]
        if json["next"] is None:
            break
    return data

@st.cache_data
def get_profile():
    url = f'https://public.tableau.com/profile/api/{PROFILE}'
    res = requests.get(url)
    json = res.json()
    return json

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def show_wb(data):
    st.image('https://public.tableau.com/thumb/views/'+data.workbookRepoUrl+'/'+data.defaultViewName)
    st.write('['+data.title+f'](https://public.tableau.com/app/profile/{PROFILE}/viz/'+data.workbookRepoUrl+'/'+data.defaultViewName+')')

def search_keyword(string,keyword):
    if keyword in string:
        return True
    else:
        return False

def show_more_mom():
    st.session_state.mom_limit += 5

def show_more_wow():
    st.session_state.wow_limit += 5

def show_more_otr():
    st.session_state.otr_limit += 5

def show_more_ser():
    st.session_state.ser_limit += 5

########################
# get data
########################
prof = get_profile()
data = get_data()
data = pd.json_normalize(data)

# make categoraized data
mom = data[
        (data['title'].apply(lambda x: search_keyword(x,'MoM')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'mom')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'MOM')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'MakeoverMonday')))
        ]
wow = data[
        (data['title'].apply(lambda x: search_keyword(x,'WoW')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'wow')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'WOW')))
        |
        (data['title'].apply(lambda x: search_keyword(x,'WorkoutWednesday')))
        ]
otr = data[
         ~(
             (data['title'].apply(lambda x: search_keyword(x,'MoM')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'mom')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'MOM')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'MakeoverMonday')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'WoW')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'wow')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'WOW')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'WorkoutWednesday')))
          )
        ]

########################
# main design
########################
st.title("My Tableau Pulbic Portfolio")

########################
# profile & summary
cols1 = st.columns([2,6,7])
with cols1[0]:
    st.write('')
    st.image(prof['avatarUrl'])
with cols1[1]:
    st.header(prof['name'])
    cols2 = st.columns(3)
    with cols2[0]:
        st.metric(label="\# of vizzes", value=len(data), label_visibility="visible")
    with cols2[1]:
        st.metric(label="Following", value=prof['totalNumberOfFollowing'])
    with cols2[2]:
        st.metric(label="Followers", value=prof['totalNumberOfFollowers'])
    cols2 = st.columns(3)
    with cols2[0]:
        st.metric('\# of MoM vizzes', len(mom))
    with cols2[1]:
        st.metric('\# of WoW vizzes', len(wow))
    with cols2[2]:
        st.metric('\# of other vizzes', len(otr))

st.write()

########################
# MakeoverMonday
num_of_mom = len(mom)
st.header(f'MakeoverMonday ({num_of_mom} vizzes)')
st.write('')

for i, chunk in enumerate(chunks(list(mom[:st.session_state.mom_limit].itertuples()),NUM_COLS)):
    cols = st.columns(NUM_COLS, gap="large")
    for c, col in zip(chunk, cols):
        with col:
            show_wb(c)
st.write('')
if st.session_state.mom_limit < len(mom):
    st.button("Show more MoM vizzes", on_click=show_more_mom, key=1, type='primary')

########################
# WorkoutWednesday
num_of_wow = len(wow)
st.header(f'WorkoutWednesday({num_of_wow} vizzes)')
st.write('')

for i, chunk in enumerate(chunks(list(wow[:st.session_state.wow_limit].itertuples()),NUM_COLS)):
    cols = st.columns(NUM_COLS, gap="large")
    for c, col in zip(chunk, cols):
        with col:
            show_wb(c)
st.write('')
if st.session_state.wow_limit < len(wow):
    st.button("Show more WoW vizzes", on_click=show_more_wow, key=2, type='primary')

########################
# Others
num_of_otr = len(otr)
st.header(f'Others({num_of_otr} vizzes)')
st.write('')

for i, chunk in enumerate(chunks(list(otr[:st.session_state.otr_limit].itertuples()),NUM_COLS)):
    cols = st.columns(NUM_COLS, gap="large")
    for c, col in zip(chunk, cols):
        with col:
            show_wb(c)
st.write('')
if st.session_state.otr_limit < len(otr):
    st.button('Show more other vizzes', on_click=show_more_otr, key=3, type='primary')

########################
# Search
st.header(f'Search')
keyword = st.text_input('')
if keyword == '':
    st.write('☝️ Please input search keyword')
else:
    ser = data[data['title'].apply(lambda x: keyword in x)]
    num_of_ser = len(ser)
    st.write(f'{num_of_ser} vizzes hit.')
    
    for i, chunk in enumerate(chunks(list(ser[:st.session_state.ser_limit].itertuples()),NUM_COLS)):
        cols = st.columns(NUM_COLS, gap="large")
        for c, col in zip(chunk, cols):
            with col:
                show_wb(c)
    st.write('')
    if st.session_state.ser_limit < len(ser):
        st.button('Show more vizzes', on_click=show_more_ser, key=4, type='primary')

