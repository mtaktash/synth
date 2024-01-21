from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

from synth.oscillator.sawtooth import SawtoothOscillator
from synth.oscillator.sine import SineOscillator
from synth.oscillator.square import SquareOscillator
from synth.oscillator.triangle import TriangleOscillator
from synth.oscillator.wave_adder import WaveAdder


def wave_to_file(
    wav: np.ndarray,
    wav2: Optional[np.ndarray] = None,
    fname: str = "temp.wav",
    amp: float = 0.1,
    sample_rate: int = 44100,
):
    wav = np.int16(wav * amp * (2**15 - 1))

    if wav2 is not None:
        wav2 = np.int16(wav2 * amp * (2**15 - 1))
        wav = np.stack([wav, wav2]).T

    wavfile.write(fname, sample_rate, wav)


def plot_wave(
    wav: np.ndarray,
    sample_every: int = 300,
    fname: str = "temp.png",
    sample_rate: int = 44100,
    duration: int = 4,
):
    plt.figure(figsize=(20, 5))
    plt.plot(wav[::sample_every])
    plt.xticks(
        np.arange(
            0, sample_rate * duration // sample_every, sample_rate // sample_every
        ),
        np.arange(duration),
    )
    plt.xlabel("Time (s)")
    plt.savefig(fname)


if __name__ == "__main__":
    sample_rate = 44100
    duration = 4

    gen = WaveAdder(
        SineOscillator(freq=440, phase=0),
        TriangleOscillator(freq=220, amp=0.8),
        SawtoothOscillator(freq=110, amp=0.6),
        SquareOscillator(freq=55, amp=0.4),
    )
    iter(gen)
    wav = [next(gen) for _ in range(sample_rate * duration)]  # 4 Seconds
    wav = np.array(wav)
    wave_to_file(wav, fname="prelude_one.wav", sample_rate=sample_rate)
    plot_wave(
        wav,
        fname="prelude_one.png",
        sample_every=300,
        sample_rate=sample_rate,
        duration=duration,
    )
