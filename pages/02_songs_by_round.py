import streamlit as st
from forumvision import df
from st_aggrid import AgGrid



st.markdown("# Songs by round")
st.sidebar.markdown("## Songs by round")

players = sorted(df['Game'].unique())

selected_round = st.sidebar.selectbox('Select a game/round', players)

st.markdown(f"### Playlist of {selected_round}")

AgGrid(df[df['Game'] == selected_round], fit_columns_on_grid_load=True)
