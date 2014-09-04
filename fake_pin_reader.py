#!/usr/bin/env python

class FakePinReader(object):
  def __init__(self, active_high=True, current_value=False):
    self.active_high = active_high
    self.current_value = current_value

  def read(self):
    return self.current_value == self.active_high

  @property
  def current_value(self):
    return self._current_value

  @current_value.setter
  def current_value(self, val):
    self._current_value = val
  
  @property
  def active_high(self):
    return self._active_high

  @active_high.setter
  def active_high(self, val):
    self._active_high = val
