import streamlit as st
import pandas as pd
import json
import requests
from streamlit_elements import nivo 

st.set_page_config(layout="wide")

# get tableau public data
@st.cache_data
def get_data():
    profile = st.secrets.PROFILE
    start = 0
    count = 50 # the number of get count is limited to 50
    data = []
    while(True):
        url_base = f'https://public.tableau.com/public/apis/workbooks?profileName={profile}&start={start}&count={count}&visibility=NON_HIDDEN'
        res = requests.get(url_base)
        json = res.json()
        start = json["next"]
        data += json["contents"]
        if json["next"] is None:
            break
    return data

data = get_data()
data = pd.json_normalize(data)

def search_keyword(string,keyword):
    if keyword in string:
        return True
    else:
        return False

# sidebar design
#with st.sidebar:
    #st.header("aa")

# main design
st.title("Tableau Pulbic Portfolio")

st.metric(label="\# of vizzes", value=len(data), label_visibility="visible")

#st.write(data)

#detail_data = []
#for row in data:
    #url = 'https://public.tableau.com/profile/api/workbook/'
    #url += row['workbookRepoUrl']
    #res = requests.get(url)
    #detail_data.append(res.json)
#
#st.write(pd.json_normalize(detail_data))

c1, c2, c3 = st.columns(3)
mom = data[data['title'].apply(lambda x: search_keyword(x,'MoM'))]
wow = data[data['title'].apply(lambda x: search_keyword(x,'WoW'))]
otr = data[
         ~(
             (data['title'].apply(lambda x: search_keyword(x,'MoM')))
             |
             (data['title'].apply(lambda x: search_keyword(x,'WoW')))
          )
        ]
with c1:
    st.subheader('MakeoverMonday')
    st.metric('\# of MoM viz', len(mom))
    st.write(mom.title)
with c2:
    st.subheader('WorkoutWednesday')
    st.metric('\# of WoW viz', len(wow))
    st.write(wow.title)
with c3:
    st.subheader('Others')
    st.metric('\# of other viz', len(otr))
    st.write(otr.title)
