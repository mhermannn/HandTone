import pygame
import numpy
import math
import time

pygame.init()

bits = 16
sample_rate = 44100

pygame.mixer.pre_init(sample_rate, bits)

def sine_x(amp, freq, time1):
    return int(round(amp * math.sin(2 * math.pi * freq * time1)))

def square_x(amp, freq, time1):
    return amp if math.sin(2 * math.pi * freq * time1) >= 0 else -amp

def triangle_x(amp, freq, time1):
    period = 1.0 / freq
    time1 = time1 % period
    value = (2 / period) * time1 - 1
    return amp * (2 * abs(value) - 1)

def sawtooth_x(amp, freq, time1):
    period = 1.0 / freq
    time1 = time1 % period
    return amp * ((time1 / period) * 2 - 1)

class Tone:
    def play(freq, duration=1, speaker=None, wave_type='sine'):
        num_samples = int(round(duration * sample_rate))
        sound_buffer = numpy.zeros((num_samples, 2), dtype = numpy.int16)
        amplitude = 2 ** (bits - 1) - 1

        for sample_num in range(num_samples):
            time1 = float(sample_num) / sample_rate

            if wave_type == 'sine':
                wave = sine_x(amplitude, freq, time1)
            elif wave_type == 'square':
                wave = square_x(amplitude, freq, time1)
            elif wave_type == 'triangle':
                wave = triangle_x(amplitude, freq, time1)
            elif wave_type == 'sawtooth':
                wave = sawtooth_x(amplitude, freq, time1)

            if speaker == 'r':
                sound_buffer[sample_num][1] = wave
            if speaker == 'l':
                sound_buffer[sample_num][0] = wave
            else:
                sound_buffer[sample_num][1] = wave
                sound_buffer[sample_num][0] = wave
        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=1, maxtime=int(duration * 1000))
        time.sleep(duration)

