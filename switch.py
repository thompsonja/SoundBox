#!/usr/bin/env python
import threading

class Switch(object):
  TRIGGER_ACTIVE = 0
  LEVEL_ACTIVE = 1
  TRIGGER_INACTIVE = 2
  LEVEL_INACTIVE = 3  

  def __init__(self, pin_reader, on_active=None, on_inactive=None, initial_state=LEVEL_INACTIVE):
    self.pin_reader = pin_reader
    self.on_active = on_active
    self.on_inactive = on_inactive
    self.is_polling = False
    self.poll_thread = threading.Thread(target=self.poller)
    self.previous = self.get_status()
    self.status = initial_state

  def get_status(self):
    return self.pin_reader.read()

  def start_polling(self):
    if self.is_polling:
      return
    self.is_polling = True
    self.poll_thread.start()

  def stop_polling(self):
    if not self.is_polling:
      return
    self.is_polling = False
    self.poll_thread.join()

  def poller(self):
    while self.is_polling:
      current = self.get_status()
      self.status = self.next_state(self.previous, current, self.pin_reader.active_high)
      if self.status == Switch.TRIGGER_ACTIVE and self.on_active:
        self.on_active()
      elif self.status == Switch.TRIGGER_INACTIVE and self.on_inactive:
        self.on_inactive()
      self.previous = current

  def next_state(self, previous, current, active_high):
    if current and not previous:
      if active_high:
        return Switch.TRIGGER_ACTIVE
      else:
        return Switch.TRIGGER_INACTIVE
    if not current and previous:
      if active_high:
        return Switch.TRIGGER_INACTIVE
      else:
        return Switch.TRIGGER_ACTIVE
    if current != active_high:
      return Switch.LEVEL_INACTIVE
    return Switch.LEVEL_ACTIVE