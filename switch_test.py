#!/usr/bin/env python
import switch
import time
import unittest

class MockReader(object):

  def __init__(self, initial_value=False):
    self.current_value = initial_value

  def read(self):
    return self.current_value

  @property
  def current_value(self):
    return self._current_value

  @current_value.setter
  def current_value(self, value):
    self._current_value = value

  @property
  def active_high(self):
    return True

  def toggle(self):
    self.current_value = not self.current_value

active_count = 0
inactive_count = 0

def active_callback():
  global active_count
  active_count += 1


def inactive_callback():
  global inactive_count
  inactive_count += 1

def reset_callbacks():
  global active_count
  global inactive_count
  active_count = 0
  inactive_count = 0


class SwitchTest(unittest.TestCase):

  def setUp(self):
    self.reader = MockReader()
    self.switch = switch.Switch(self.reader, active_callback, inactive_callback)
    self.switch.start_polling()
    pass

  def tearDown(self):
    self.reader.current_value = False
    self.switch.stop_polling()
    reset_callbacks()

  def testOneToggle(self):
    self.toggle()
    self.assertEqual(active_count, 1)
    self.assertEqual(inactive_count, 0)

  def testTwoToggles(self):
    self.toggle()
    self.toggle()
    self.assertEqual(active_count, 1)
    self.assertEqual(inactive_count, 1)

  def testUpdateState(self):
    self.assertEqual(self.switch.next_state(True, True, True), switch.Switch.LEVEL_ACTIVE)
    self.assertEqual(self.switch.next_state(True, True, False), switch.Switch.LEVEL_INACTIVE)
    self.assertEqual(self.switch.next_state(True, False, True), switch.Switch.TRIGGER_INACTIVE)
    self.assertEqual(self.switch.next_state(True, False, False), switch.Switch.TRIGGER_ACTIVE)
    self.assertEqual(self.switch.next_state(False, True, True), switch.Switch.TRIGGER_ACTIVE)
    self.assertEqual(self.switch.next_state(False, True, False), switch.Switch.TRIGGER_INACTIVE)
    self.assertEqual(self.switch.next_state(False, False, True), switch.Switch.LEVEL_INACTIVE)
    self.assertEqual(self.switch.next_state(False, False, False), switch.Switch.LEVEL_ACTIVE)

  def toggle(self):
    self.reader.toggle()
    time.sleep(1)


def runtests():
  unittest.main()

if __name__ == '__main__': runtests()