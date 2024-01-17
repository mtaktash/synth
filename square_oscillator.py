import math

from sine_oscillator import SineOscillator


class SquareOscillator(SineOscillator):
    def __init__(
        self,
        freq: float = 440.0,
        phase: int = 0,
        amp: float = 1.0,
        sample_rate: int = 44100,
        wave_range: tuple[int, int] = (-1, 1),
        threshold: float = 0.0,
    ):
        super().__init__(freq, phase, amp, sample_rate, wave_range)
        self.threshold = threshold

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if val < self.threshold:
            val = self._wave_range[0]
        else:
            val = self._wave_range[1]
        return val * self._a
