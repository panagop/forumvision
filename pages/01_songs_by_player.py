import streamlit as st
import pandas as pd
import altair as alt
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking

from forumvision import engine, session

st.markdown("# Κομμάτια ανά παίκτη ανά παιχνίδι")
st.sidebar.markdown("## Κομμάτια ανά παίκτη ανά παιχνίδι")


# engine = create_engine('sqlite:///data/forumvision.db',
#                 echo=False,
#                 connect_args={'check_same_thread': False})
# session = Session(engine)


players = [p.id for p in session.query(Player).all()]

games = [g.id for g in session.query(Game).all()]

# players = sorted(df['Player'].unique())



# select the player
selected_player = st.sidebar.selectbox('Select a player', players)

selected_game = st.sidebar.selectbox('Select a game', games)

# chart options
chart_option = st.sidebar.radio('Chart option', ['Points', 'Position'])
chart_text_option = st.sidebar.radio('Chart text', ['Title', 'Artist'])

query = session.query(
                    Song.artist.label('Artist'), 
                    Song.title.label('Title'),
                    Song.player_id.label('Player'), 
                    Song.gyros_id.label('Round'),
                    SongRanking.points.label('Points'),
                    SongRanking.position.label('Pos'),
                    Song.id.label('song_id')) \
        .join(SongRanking) \
        .filter(Song.player_id==selected_player) \
        .filter(Song.gyros_id.contains(selected_game))

df = pd.read_sql(query.statement, engine)


st.markdown(f"### Επιλογή παίκτη: {selected_player}")

# Table
st.markdown(f"#### τι διάλεξε")

# display the table
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single',use_checkbox=False)
gridoptions = gd.build()

grid_table = AgGrid(df,
                    gridOptions=gridoptions,
                    fit_columns_on_grid_load=False,
                    theme = 'streamlit',
                    update_mode= GridUpdateMode.SELECTION_CHANGED)


# Chart
st.markdown(f"#### ...και τι κατάφερε")

# prepare the chart
chart = alt.Chart(df, width=600).mark_bar().encode(
    x=chart_option,
    y='Round'
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
