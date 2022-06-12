# Contents of ~/my_app/streamlit_app.py
import streamlit as st
import pandas as pd
import os.path
import gspread
from gspread_dataframe import get_as_dataframe
import json


# df = pd.read_excel("data/forumvision.xlsx")

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        creds = json.load(f)
    # st.write(jjj)

    # sa = gspread.service_account(filename='credentials.json')
    sa = gspread.service_account_from_dict(creds)
    sh =sa.open("forumvision")
    wks = sh.worksheet(title="Sheet1")
    df = get_as_dataframe(wks, usecols=[0,1,2,3,4,5])
    # print('loaded from google sheet')
else:
    df = pd.read_excel("data/forumvision.xlsx")
    # print('loaded from local file')
    st.write(st.secrets.creds.to_dict())

def main_page():
    st.markdown("# Forumvision - full table")
    st.sidebar.markdown("# Forumvision - full table")
    st.dataframe(df)


if __name__ == "__main__":
    main_page()
