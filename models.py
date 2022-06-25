from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base, relationship, backref


Base = declarative_base()


def create_custom_view(engine, query_statement, view_name:str):
    text = f'DROP TABLE IF EXISTS {view_name}'
    with engine.connect() as conn:
        conn.execute(text)

    text = f'CREATE VIEW {view_name} AS ' + str(query_statement)
    with engine.connect() as conn:
        conn.execute(text)

    
class Game(Base):
    
    __tablename__ = 'game'
    
    id = Column(String, primary_key=True)
    gyroi = relationship("Gyros", backref="game")
    
    def __init__(self, id):
        self.id = id  

    def __repr__(self):
        return f'Game ID: {self.id}'
    
        
class Gyros(Base):
    # το Round είναι συνάρτηση όταν είναι με μικρό
    
    __tablename__ = 'gyros'
    
    id = Column(String, primary_key=True)
    url = Column(String)  
    game_id = Column(String, ForeignKey('game.id')) 
    
    songs = relationship("Song", backref="gyros")
    
    def __init__(self, id, url, game_id):
        self.id = id  
        self.url = url  
        self.game_id = game_id

    def __repr__(self):
        return f'Gyros ID: {self.id}'
    
    
class Player(Base):
    
    __tablename__ = 'player'
    
    id = Column(String, primary_key=True)
    
    songs = relationship("Song", backref="player")
    grades = relationship("Grade", backref="player")
    gyrocomments = relationship("GyroComment", backref="player")
    
    def __init__(self, id):
        self.id = id  
    
    def __repr__(self):
        return f'Player ID: {self.id}'
    
    
class Song(Base):

    __tablename__ = 'song'

    id = Column(String, primary_key=True)
    artist = Column(String) 
    title = Column(String)  
    url = Column(String)  
    player_id = Column(String, ForeignKey('player.id'))  
    gyros_id = Column(String, ForeignKey('gyros.id'))  
    duration = Column(Integer, nullable=True)
    
    grades = relationship("Grade", backref="song")

    def __init__(self, id, artist, title, url, player_id, gyros_id, duration):
        self.id = id    
        self.artist = artist   
        self.title = title   
        self.url = url   
        self.player_id = player_id
        self.gyros_id = gyros_id
        self.duration = duration

    def __repr__(self):
        return f'{self.id} submitted by {self.player_id} - Artist: {self.artist} - Title: {self.title}'
    

class Grade(Base):
    
    __tablename__ = 'grade'
    
    # id = Column(Integer, primary_key=True)
    song_id = Column(String, ForeignKey('song.id'), primary_key=True) 
    grader_id = Column(String, ForeignKey('player.id'), primary_key=True) 
    grade = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    
    def __init__(self, song_id, grader_id, grade=None, comment=None):
        self.song_id = song_id 
        self.grader_id = grader_id 
        self.grade = grade 
        self.comment = comment 
        
    def __repr__(self):
        text = r'Ο/Η/Το ' +  f'{self.grader_id} βαθμολόγησε με {self.grade} '
        if self.comment is not None:
            text += f'και σχολίασε: {self.comment}'
        return text
        # return f'Song {self.song_id} got {self.grade} points by {self.grader_id}'
        

class GyroComment(Base):
    
    __tablename__ = 'gyrocomment'
    
    gyros_id = Column(String, ForeignKey('gyros.id'), primary_key=True)
    player_id = Column(String, ForeignKey('player.id'), primary_key=True)
    comment = Column(String, nullable=True)
    
    def __init__(self, gyros_id, player_id, comment=None):
        self.gyros_id = gyros_id 
        self.player_id = player_id 
        self.comment = comment 
    
    def __repr__(self):
        return f'Player {self.player_id} commented for round {self.gyros_id}: {self.comment}'


class SongRanking(Base):
    
    __tablename__ = 'song_ranking'
    
    song_id = Column(String, ForeignKey('song.id'), primary_key=True) 
    # gyros_id = Column(String, ForeignKey('gyros.id'), primary_key=True)
    # player_id = Column(String, ForeignKey('player.id'))
    points = Column(Integer, nullable=True)
    position = Column(Integer, nullable=True)
    
    song = relationship("Song", backref=backref("song_ranking", uselist=False))

    
    def __init__(self, song_id, points, position):
        self.song_id = song_id 
        # self.gyros_id = gyros_id 
        # self.player_id = player_id 
        self.points = points 
        self.position = position 
        
        
class PlayerRanking(Base):
    
    __tablename__ = 'player_ranking'    
    
    song_id = Column(String, ForeignKey('song.id')) 
    player_id = Column(String, ForeignKey('player.id'), primary_key=True)
    gyros_id = Column(String, ForeignKey('gyros.id'), primary_key=True)
    game_id = Column(String, ForeignKey('game.id')) 
    points = Column(Integer, ForeignKey('song_ranking.points'), nullable=True)
    sum_points = Column(Integer, nullable=True)
    player_position = Column(Integer, nullable=True)
    
    
    def __init__(self, song_id, player_id, gyros_id, game_id, points, sum_points, player_position):
        self.song_id = song_id 
        self.player_id = player_id 
        self.gyros_id = gyros_id 
        self.game_id = game_id 
        self.points = points 
        self.sum_points = sum_points 
        self.player_position = player_position 

