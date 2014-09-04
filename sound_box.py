#!/usr/bin/env python
# import digital_pin_reader
import sound_player
import switch

class SoundBox(object):

  def __init__(self, songs, input_pin=11, active_high=True, test=False):
    self.sound_player = sound_player.SoundPlayer(songs)
    if test:
      import fake_pin_reader
      self.pin_reader = fake_pin_reader.FakePinReader(active_high=active_high)
    else:
      import digital_pin_reader
      self.pin_reader = digital_pin_reader.DigitalPinReader(input_pin, active_high)
    self.switch = switch.Switch(self.pin_reader, on_active=self.sound_player.next)

  def start(self):
    self.switch.start_polling()

  def stop(self):
    self.switch.stop_polling()
    self.sound_player.stop()

if __name__ == '__main__':
  sound_box = SoundBox(['0.mp3', '1.mp3'])
  sound_box.start()
  