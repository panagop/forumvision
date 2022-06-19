import os.path
import json
import streamlit as st
import gspread
from gspread_dataframe import get_as_dataframe
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Gyros, Song
import pandas as pd

# # Alternative option: Load data from Excel file
# df = pd.read_excel("data/forumvision.xlsx")

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        creds = json.load(f)
    # # or directly from the json file
    # sa = gspread.service_account(filename='credentials.json')
else:
    creds = dict(st.secrets.creds)

engine = create_engine('sqlite:///data/forumvision.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)

sa = gspread.service_account_from_dict(creds)
sh = sa.open("forumvision")
wks = sh.worksheet(title="Sheet1")
df = get_as_dataframe(wks, usecols=[0, 1, 2, 3, 4, 5])


def main_page():
    st.sidebar.markdown("# Forumvision - Main page")

    st.markdown("# Forumvision - Main page")
    st.markdown("## All games - Full table")
    st.dataframe(df)

    st.markdown("## All games - Full Song table with SQL")
    df2 = pd.read_sql(session.query(Song).statement, engine, index_col='id')
    st.dataframe(df2)


if __name__ == "__main__":
    main_page()
