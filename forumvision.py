﻿# import os.path
# import json
# import gspread
# from gspread_dataframe import get_as_dataframe
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking



st.set_page_config(page_title="forumvision statistics", layout="centered")


## older version....using google sheets

# if os.path.exists('credentials.json'):
#     with open('credentials.json') as f:
#         creds = json.load(f)
#     # # or directly from the json file
#     # sa = gspread.service_account(filename='credentials.json')
# else:
#     creds = dict(st.secrets.creds)

# sa = gspread.service_account_from_dict(creds)
# sh = sa.open("forumvision")
# wks = sh.worksheet(title="Sheet1")
# df = get_as_dataframe(wks, usecols=[0, 1, 2, 3, 4, 5])

# end of older version....using google sheets 


# # Alternative older version....: Load data from Excel file
# df = pd.read_excel("data/forumvision.xlsx")


engine = create_engine('sqlite:///data/forumvision.db',
                echo=False,
                connect_args={'check_same_thread': False})
session = Session(engine)

# query = session.query(Grade.song_id,
#                     Song.artist.label('Artist'), 
#                     Song.title.label('Title'),
#                     Song.player_id.label('Player'), 
#                     Song.gyros_id.label('Game'),
#                     func.sum(Grade.grade).label('Points'),
#                     func.rank().over(
#                     partition_by=Song.gyros_id,
#                     order_by=func.sum(Grade.grade).desc())
#                     .label('Pos'), 
#                     Song.url) \
#     .join(Song) \
#     .group_by(Grade.song_id) \
#     .order_by(Song.gyros_id, desc('Points'))


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

df = pd.read_sql(query.statement, engine)


# def main_page():
st.sidebar.markdown("# Main page")
st.sidebar.markdown('Επιλέγοντας κομμάτι στον πίνακα εμφανίζεται το βίντεο, οι βαθμολογίες και τα σχόλια')

st.markdown("# Main page")
st.markdown("## All games - Full table")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single',use_checkbox=False)
gridoptions = gd.build()

grid_table = AgGrid(df,
                    gridOptions=gridoptions,
                    fit_columns_on_grid_load=False,
                    theme = 'streamlit',
                    height=500,
                    update_mode= GridUpdateMode.SELECTION_CHANGED)

sel_row = grid_table["selected_rows"]

try:
    st.video(sel_row[0]['url'])
    q = session.query(Song).filter(Song.id == sel_row[0]['song_id']).one()
    for gr in q.grades:
        st.write(gr)

except:
    pass


    # st.markdown("## All games - Full Song table with SQL")
    # df2 = pd.read_sql(session.query(Song).statement, engine, index_col='id')
    # st.dataframe(df2)


# if __name__ == "__main__":
#     main_page()
