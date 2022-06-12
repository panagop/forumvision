import streamlit as st
from forumvision import df

st.markdown("# Songs by round")
st.sidebar.markdown("## Songs by round")

players = sorted(df['Game'].unique())

selected_round = st.sidebar.selectbox('Select a game/round', players)

st.markdown(f"### Playlist of {selected_round}")

st.dataframe(df[df['Game'] == selected_round])
