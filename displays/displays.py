import streamlit as st
import matplotlib.pyplot as plt

from models import Base, Song, Game, Gyros, Player, Grade, GyroComment
from models import SongRanking, PlayerRanking



def show_video(url):
    st.video(url)


def show_song_grades(session, song_id):
    q = session.query(Song).filter(Song.id == song_id).one()
    for grade in q.grades:
        st.write(grade)


def improve_legend(ax=None):
    """
    https://stackoverflow.com/questions/49237522/how-to-annotate-end-of-lines-using-python-and-matplotlib
    """

    if ax is None:
        ax = plt.gca()

    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
        
    for line in ax.lines:
        data_x, data_y = line.get_data()
        right_most_x = data_x[-1]
        right_most_y = data_y[-1]
        ax.annotate(
            line.get_label(),
            xy=(right_most_x, right_most_y),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            color=line.get_color(),
        )
    ax.legend().set_visible(False)