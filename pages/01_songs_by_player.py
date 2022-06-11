# Contents of ~/my_app/pages/page_2.py
import streamlit as st
import pandas as pd
from forumvision import df

st.markdown("# Songs by player")
st.sidebar.markdown("## Songs by player")

players = sorted(df['Player'].unique())

selected_player = st.selectbox('Select a player', players)

st.markdown(f"### {selected_player}")

st.dataframe(df[df['Player']==selected_player])

