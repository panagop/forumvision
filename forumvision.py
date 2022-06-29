# import os.path
# import json
# import gspread
# from gspread_dataframe import get_as_dataframe
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import insert, func, desc
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking

from axaxa import create_session
from displays.displays import show_video, show_song_grades

st.set_page_config(page_title="forumvision statistics", layout="centered")

# def main_page():
st.sidebar.markdown("# Main page")
st.sidebar.markdown('Επιλέγοντας κομμάτι στον πίνακα εμφανίζεται το βίντεο, οι βαθμολογίες και τα σχόλια')

st.markdown("# Main page")
st.markdown("## All games - Full table")


# Load the data
engine, session = create_session()

# Query the data
query = session.query(
                    Song.artist.label('Artist'), 
                    Song.title.label('Title'),
                    Song.player_id.label('Player'), 
                    Song.gyros_id.label('Round'),
                    SongRanking.points.label('Points'),
                    SongRanking.position.label('Pos'),
                    Song.url,
                    Song.id.label('song_id')) \
        .join(SongRanking)

# Convert to dataframe
df = pd.read_sql(query.statement, engine)

# Create the grid
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single',use_checkbox=False)
gridoptions = gd.build()

grid_table = AgGrid(df,
                    gridOptions=gridoptions,
                    fit_columns_on_grid_load=False,
                    theme = 'streamlit',
                    height=500,
                    update_mode= GridUpdateMode.SELECTION_CHANGED)

# Show info for the selected song
sel_row = grid_table["selected_rows"]

if sel_row:
    video_url = sel_row[0]['url']
    song_id = sel_row[0]['song_id']

    show_video(video_url)
    show_song_grades(session, song_id)





# if __name__ == "__main__":
#     main_page()
