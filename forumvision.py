import os.path
import streamlit as st
import gspread
from gspread_dataframe import get_as_dataframe
import json

# # Alternative option: Load data from Excel file
# df = pd.read_excel("data/forumvision.xlsx")

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        creds = json.load(f)
    # # or directly from the json file
    # sa = gspread.service_account(filename='credentials.json')
else:
    creds = dict(st.secrets.creds)
    

sa = gspread.service_account_from_dict(creds)
sh =sa.open("forumvision")
wks = sh.worksheet(title="Sheet1")
df = get_as_dataframe(wks, usecols=[0,1,2,3,4,5])


def main_page():
    st.sidebar.markdown("# Forumvision - Main page")
    
    st.markdown("# Forumvision - Main page")
    st.markdown("## All games - Full table")
    st.dataframe(df)


if __name__ == "__main__":
    main_page()
