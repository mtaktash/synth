import random

import numpy as np
import pygame as pg

from sine_oscillator import SineOscillator


def generate_note(freq: float):
    sample_rate = 44100
    duration = 1
    amp = 0.1
    osc = SineOscillator(freq=freq)
    gen = iter(osc)
    wav = [next(gen) for _ in range(sample_rate * duration)]
    wav = np.array(wav)
    wav = np.int16(wav * amp * (2**15 - 1))
    return np.asarray([wav, wav]).T


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


NOTES_TO_FREQS = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}


if __name__ == "__main__":
    screen_width, screen_height = 1280, 720

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    font = pg.font.SysFont("comicsans", 48)

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False

            if event.type == pg.KEYDOWN:
                key = str(event.unicode)
                note = key.upper()

                if note in NOTES_TO_FREQS:
                    wav = generate_note(NOTES_TO_FREQS[note])

                    note_screen = font.render(note, True, random_color())
                    note_screen_rect = note_screen.get_rect()
                    note_screen_rect.center = (
                        random.randint(0, screen_width),
                        random.randint(0, screen_height),
                    )
                    screen.blit(note_screen, note_screen_rect)

                    pg.display.update()
                    pg.sndarray.make_sound(wav.copy()).play()

        pg.display.update()

    pg.mixer.quit()
    pg.quit()
