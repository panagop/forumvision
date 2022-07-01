import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

from displays.displays import improve_legend

# from forumvision import engine, session

from axaxa import create_session
engine, session = create_session()

sns.set_style("darkgrid", {"axes.facecolor": ".9"})

st.markdown('# Εξέλιξη βαθμολογίας ανά παιχνίδι')

games = [g.id for g in session.query(Game).all()]

selected_game = st.sidebar.selectbox('Select a game', games, index=len(games)-1)

query = session.query(PlayerRanking).filter(PlayerRanking.game_id==selected_game)
df = pd.read_sql(query.statement, engine)
# st.dataframe(df)

players_option = st.sidebar.radio('Players Option', ['All players', 'Selected players'])

players = sorted(list(df['player_id'].unique()))

if players_option=='All players':
    selected_players = players
else:
    selected_players = st.sidebar.multiselect('select players', players, default=players)


query = query.filter(PlayerRanking.player_id.in_(selected_players))
df = pd.read_sql(query.statement, engine)
# st.dataframe(df)


chart_type_option = st.radio('Chart type', ['Static', 'Interactive'], index=1)

# try:
chart_include_names = st.checkbox('Include names on chart', value=False)

if chart_type_option == 'Static':
    fig, ax = plt.subplots()
    df.pivot_table('sum_points', index='gyros_id', columns='player_id', aggfunc='sum').plot(ax=ax, figsize=(12,8))
    if chart_include_names: improve_legend(ax)
    st.pyplot(fig)
else:
    
    chart = alt.Chart(df, height=600).transform_window(
            cumulative='sum(points)',
            sort=[{"field": "gyros_id"}],
            groupby=['player_id'],
        ).mark_line().encode(
            x='gyros_id:N',
            y='cumulative:Q',
            color='player_id:N',
            text='player_id:N',
        )

    if chart_include_names:
        chart = chart+chart.mark_text(align='left', dx=5).encode(
            text='player_id:N')

    st.altair_chart(chart.interactive(), use_container_width=True)

# except:
#     pass






