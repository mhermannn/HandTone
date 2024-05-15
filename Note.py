from Tone import Tone
from utils import NOTE_MAP

class Note:
    def __init__(self, note_str, duration=1):
        main_note = note_str[0].upper()
        self.note_str = main_note + note_str[1:]
        self.duration = duration
        self.freq = NOTE_MAP[self.note_str]

    def play(self, wave_type='sine', speaker=None):
        Tone.play(self.freq, duration=self.duration, speaker=speaker, wave_type=wave_type)
