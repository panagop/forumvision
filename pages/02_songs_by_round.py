# Contents of ~/my_app/pages/page_2.py
import streamlit as st
import pandas as pd
from forumvision import df

st.markdown("# Songs by round")
st.sidebar.markdown("## Songs by round")

players = sorted(df['Game'].unique())

selected_round = st.selectbox('Select a game/round', players)

st.markdown(f"### {selected_round}")

st.dataframe(df[df['Game']==selected_round])
