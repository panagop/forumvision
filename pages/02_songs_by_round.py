import streamlit as st
# from forumvision import df
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking

from displays.displays import show_video, show_song_grades

# from forumvision import engine, session
from axaxa import create_session
engine, session = create_session()

# Query the data
query = session.query(
                    SongRanking.position.label('Position'),
                    SongRanking.points.label('Points'),
                    Song.artist.label('Artist'), 
                    Song.title.label('Title'),
                    Song.player_id.label('Player'), 
                    Song.gyros_id.label('Round'),
                    Song.url,
                    Song.id.label('song_id')) \
        .join(SongRanking)

# Convert to dataframe
df = pd.read_sql(query.statement, engine)

st.markdown("# Κομμάτια ανά γύρο")
st.sidebar.markdown("## Κομμάτια ανά γύρο")

rounds = [g.id for g in session.query(Gyros).all()]

selected_round = st.sidebar.selectbox('Select a game/round', rounds)

st.markdown(f"### Playlist of {selected_round}")

# display the table
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single',use_checkbox=False)
gridoptions = gd.build()

grid_table = AgGrid(df[df['Round'] == selected_round],
                    gridOptions=gridoptions,
                    fit_columns_on_grid_load=False,
                    theme = 'streamlit',
                    update_mode= GridUpdateMode.SELECTION_CHANGED)

# AgGrid(df[df['Round'] == selected_round], fit_columns_on_grid_load=True)

# Show info for the selected song
sel_row = grid_table["selected_rows"]

if sel_row:
    video_url = sel_row[0]['url']
    song_id = sel_row[0]['song_id']

    show_video(video_url)
    show_song_grades(session, song_id)

