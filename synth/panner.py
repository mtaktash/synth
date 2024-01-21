class Panner:
    def __init__(self, r: float = 0.5):
        self.r = r

    def __call__(self, val: float):
        r = self.r * 2
        l = 2 - r
        return (l * val, r * val)
