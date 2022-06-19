from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

       
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
        return f'Song {self.song_id} got {self.grade} points by {self.grader_id}'
        

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



