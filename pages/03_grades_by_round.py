import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from sqlalchemy import create_engine
from sqlalchemy import insert, func, desc
from sqlalchemy.orm import Session
from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking

# from forumvision import engine, session
from axaxa import create_session
engine, session = create_session()



# st.set_page_config(layout="wide")

st.markdown('## Βαθμολογίες ανά γύρο')

rounds = [g.id for g in session.query(Gyros).all()]

selected_round = st.sidebar.selectbox('Select a game/round', rounds)

st.markdown(f"### Results of {selected_round}")


query = session.query(
                    Grade.song_id, 
                    Grade.grader_id,
                    Grade.grade,
                    Song.artist,
                    Song.title,
                    Song.gyros_id.label('Round')) \
        .join(Song)

query = query.filter(Song.gyros_id==selected_round)
df = pd.read_sql(query.statement, engine)

ddf = df.pivot_table(index=['artist', 'title'], columns='grader_id',
                    aggfunc={'grade':sum})
ddf['Total'] = ddf[list(ddf.columns)].sum(axis=1)

ddf.reset_index(inplace=True)


st.dataframe(ddf.sort_values(by=['Total'], ascending=False))

# df2 = df.groupby(['song_id', 'grader_id'])['grade'].aggregate('sum').unstack()
# df2['Total'] = df2[list(df2.columns)].sum(axis=1)

# df3 = pd.merge(df,df2, left_on='song_id', right_on='song_id')

# st.dataframe(df3.sort_values(by=['Total'], ascending=False))