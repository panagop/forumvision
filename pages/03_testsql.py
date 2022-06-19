import streamlit as st
import pandas as pd

from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from forumvision import session, engine


st.markdown('## Σχόλια γύρων')
df2 = pd.read_sql(session.query(GyroComment).statement, engine)
st.dataframe(df2)

