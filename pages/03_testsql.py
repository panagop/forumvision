import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from forumvision import session, engine


st.markdown('## Βαθμοί')
df2 = pd.read_sql(session.query(Grade).statement, engine)
# st.write(df2)
# st.dataframe(df2)

AgGrid(df2, fit_columns_on_grid_load=True)
