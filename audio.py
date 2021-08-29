import numpy as np
import librosa
import librosa.display
import librosa.util
import soundfile as sf


import matplotlib.pyplot as plt
fig, ax = plt.subplots(nrows=3, sharex=True)

# make_frame = lambda t: 2*[ np.sin(440 * 2 * np.pi * t) ]
# clip = AudioClip(make_frame, duration=5,fps=44100)

fn = 'E:/00IT/P/棋雀/src/video/download/【中国象棋】北昆仑刘殿中vs外星人王天一 千古名局 飞刀大战 绝无仅有.mp3'


y, sr = librosa.load(fn,sr=None,duration=50)

b = librosa.effects.pitch_shift(y, sr, n_steps=-3)

# sf.write("gg_resample.wav",y,sr*2,subtype='PCM_24')
sf.write("gg_resample_14.wav",b,sr,subtype='PCM_24')
