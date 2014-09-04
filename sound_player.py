#!/usr/bin/env python
import pygame

class SoundPlayer(object):

  def __init__(self, songs):
    pygame.mixer.init()
    self.songs = songs
    if songs is None or len(songs) == 0:
      raise Exception('Invalid song list')
    self.song_index = 0

  def play(self):
    pygame.mixer.music.load(self.songs[self.song_index])
    pygame.mixer.music.play()

  def stop(self):
    pygame.mixer.music.stop()

  def next(self):
    print 'playing next song'
    self.song_index = (self.song_index + 1) % len(self.songs)
    self.stop()
    self.play()

a = SoundPlayer(['0.mp3', '1.mp3'])