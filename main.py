import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

from synth.oscillator.modulated import ModulatedOscillator
from synth.oscillator.sawtooth import SawtoothOscillator
from synth.oscillator.sine import SineOscillator
from synth.oscillator.square import SquareOscillator
from synth.oscillator.triangle import TriangleOscillator
from synth.oscillator.wave_adder import WaveAdder
from synth.panner import Panner
from synth.param_mod import amp_mod, freq_mod


def wave_to_file(
    wav: np.ndarray,
    wav2: np.ndarray | None = None,
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
    if wav.ndim == 1:
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

    else:
        wav_left = wav[:, 0]
        wav_right = wav[:, 1]

        plt.figure(figsize=(20, 10))
        plt.subplot(2, 1, 1)
        plt.plot(wav_left[::sample_every])
        plt.ylabel("Left Channel")
        plt.xticks([])

        plt.subplot(2, 1, 2, sharey=plt.gca())
        plt.plot(wav_right[::sample_every])
        plt.ylabel("Right Channel")
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

    gen = ModulatedOscillator(
        SquareOscillator(freq=110),
        SawtoothOscillator(freq=5, wave_range=(0.2, 1)),
        amp_mod=amp_mod,
    )
    panner = Panner(r=0.3)
    iter(gen)

    wav = [panner(next(gen)) for _ in range(sample_rate * duration)]  # 4 Seconds
    wav = np.array(wav)

    wave_to_file(wav, fname="prelude_one.wav", sample_rate=sample_rate)
    plot_wave(
        wav,
        fname="prelude_one.png",
        sample_every=300,
        sample_rate=sample_rate,
        duration=duration,
    )
