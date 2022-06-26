﻿import streamlit as st
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

from forumvision import engine, session

st.set_page_config(layout="centered")

st.markdown('Εξέλιξη βαθμολογίας ανά παιχνίδι')

games = [g.id for g in session.query(Game).all()]

selected_game = st.sidebar.selectbox('Select a game', games)

query = session.query(PlayerRanking).filter(PlayerRanking.game_id==selected_game)
df = pd.read_sql(query.statement, engine)
# st.dataframe(df)

players_option = st.sidebar.radio('Players Option', ['All players', 'Selected players'])

players = list(df['player_id'].unique())

if players_option=='All players':
    selected_players = players
else:
    selected_players = st.sidebar.multiselect('select players', players, default=players)


query = query.filter(PlayerRanking.player_id.in_(selected_players))
df = pd.read_sql(query.statement, engine)
# st.dataframe(df)

try:
    fig, ax = plt.subplots()
    df.pivot_table('sum_points', index='gyros_id', columns='player_id', aggfunc='sum').plot(ax=ax, figsize=(12,8))
except:
    pass

st.pyplot(fig)