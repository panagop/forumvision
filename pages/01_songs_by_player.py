import streamlit as st
import pandas as pd
from forumvision import df
import altair as alt

st.markdown("# Songs by player")
st.sidebar.markdown("## Songs by player")

players = sorted(df['Player'].unique())

# select the player
selected_player = st.sidebar.selectbox('Select a player', players)

# chart options
chart_option = st.sidebar.radio('Chart option', ['Points', 'Position'])
chart_text_option = st.sidebar.radio('Chart text', ['Title', 'Artist'])

st.markdown(f"### Επιλογή παίκτη: {selected_player}")

# Table
st.markdown(f"#### τι διάλεξε")

# get the player's songs and display the table
df_player = df[df['Player'] == selected_player]
st.dataframe(df_player)

# Chart
st.markdown(f"#### ...και τι κατάφερε")

# prepare the chart
chart = alt.Chart(df_player, width=600).mark_bar().encode(
    x=chart_option,
    y='Game'
)

text = chart.mark_text(
    align='left',
    baseline='middle',
    color='green',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text=str(chart_text_option)
)

# display the chart
st.altair_chart((chart+text))
