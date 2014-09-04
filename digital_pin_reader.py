#!/usr/bin/env python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class DigitalPinReader(object):
  def __init__(self, input_pin, active_high=True):
    pullupdown = GPIO.PUD_DOWN if active_high else GPIO.PUD_UP
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=pullupdown)
    self.active_high = active_high
    self.input_pin = input_pin

  def read(self):
    return (GPIO.input(self.input_pin) == 1) != self.active_high
  
  @property
  def active_high(self):
    return self._active_high

  @active_high.setter
  def active_high(self, value):
    self._active_high = value