import streamlit as st
import pandas as pd
import pickle
from feature import get_all_features
import time
from PIL import Image

start = time.time()
st.set_page_config(layout="wide")
@st.cache
def get_features(url):
        data = get_all_features(url)
        return(data)

st.title('Phishing Website Detector')

st.sidebar.title('User Input Features')


st.sidebar.title('Use URL for prediction')
url = st.sidebar.text_area('URL')
url = url.split('%0A')[0]

st.sidebar.write('OR')

st.sidebar.subheader('Manually input features for prediction')
ssl_cert = st.sidebar.slider('SSL Certificate', -1, 1, 0, step = 1)
dom_reg_len = st.sidebar.slider('Domain Registeration Length', 0, 1, 0, step = 1)
url_anchor = st.sidebar.slider('URL of Anchor', -1, 1, 0, step = 1)
pref_suff = st.sidebar.slider('Prefix Suffix', -1, 1, 0, step = 1)
web_traf = st.sidebar.slider('Web Traffic', -1, 1, 0, step = 1)

data = {'SSLfinal_State': ssl_cert,
        'Domain_registeration_length': dom_reg_len,
        'URL_of_Anchor': url_anchor,
        'Prefix_Suffix': pref_suff,
        'web_traffic': web_traf}

st.subheader('Features Input by User')

if url:
        data31 = get_all_features(url)
        st.write(f"The website entered by the user is {url}")
        st.dataframe(data31)

        model31 = pickle.load(open('model31.pkl', 'rb'))

        pred = model31.predict(data31)
        pred_prob = model31.predict_proba(data31)
        
        st.subheader('Is the website youre visiting going to steal your data?')
        if pred == 0:
                if(pred_prob[0][0]>0.7):
                        st.success(f"No the website you're visiting is safe have a happy surfing. I'm like {round(pred_prob[0][0]*100,2)}% sure of that!!!")
                else:
                        st.warning(f"The website you're visiting might steal your data! Please be careful while surfing. I'm like {round(pred_prob[0][0]*100,2)}% sure of that!!!")
        else:
                st.error(f"This website is probably going to steal your data. I'm like {round(pred_prob[0][1]*100,2)}% sure of that!!!")
        end31 = time.time()
        st.subheader("Time Taken for Prediction")
        st.write(f"This check costed you {round(end31-start,2)} seconds of your precious time.")

else:
        data5 = pd.DataFrame(data, index=[0])

        st.dataframe(data5)

        model5 = pickle.load(open('model5.pkl', 'rb'))
        pred = model5.predict(data5)
        pred_prob = model5.predict_proba(data5)
        

        st.subheader('Is the website youre visiting going to steal your data?')
        if pred == 0:
                if(pred_prob[0][0]>0.7):
                        st.success(f"No the website you're visiting is safe have a happy surfing. I'm like {round(pred_prob[0][0]*100,2)}% sure of that!!!")
                else:
                        st.warning(f"The website you're visiting might steal your data! Please be careful while surfing. I'm like {round(pred_prob[0][0]*100,2)}% sure of that!!!")
        else:
                st.error(f"This website is probably going to steal your data. I'm like {round(pred_prob[0][1]*100,2)}% sure of that!!!")
        end5 = time.time()
        st.subheader("Time Taken for Prediction")
        st.write(f"This check costed you {round(end5-start,2)} seconds of your precious time.")

if st.button('Show Feature Selection Plot'):
        image = Image.open("newplot.jpg")
        st.image(image, width = 1400)