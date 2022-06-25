import streamlit as st
from forumvision import df
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking



st.markdown("# Κομμάτια ανά γύρο")
st.sidebar.markdown("## Κομμάτια ανά γύρο")

players = sorted(df['Round'].unique())

selected_round = st.sidebar.selectbox('Select a game/round', players)

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
