from synth.envelope.adsr import ADSREnvelope


def amp_mod(init_amp: float, env: ADSREnvelope):
    return env * init_amp


def freq_mod(
    init_freq: float,
    env: ADSREnvelope,
    mod_amt: float = 0.01,
    sustain_level: float = 0.7,
):
    return init_freq + ((env - sustain_level) * init_freq * mod_amt)
