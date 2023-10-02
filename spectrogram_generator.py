
import os
import sys
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram

def create_save_spectrogram(song,song_name,folder):
    plt.interactive(False)
    clip, sample_rate = librosa.load(song, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.specgram(clip,NFFT=512, Fs=2, Fc=0, noverlap=128, cmap='inferno', mode='psd')
    ax.axis('off')
    ax.grid(False)
    ax.set_frame_on(False)
    fig.canvas.draw()
    size = fig.get_size_inches()*fig.dpi
    buf = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
    buf = buf.reshape(fig.canvas.get_width_height()[::-1]+ (3,))
    buf = np.array(buf)
    plt.close(fig)
    buf = buf.astype(np.float32)/255.

    filename = os.path.splitext(os.path.basename(song_name))[0]
    outfile = os.path.join(folder, "{}.png".format(filename))
    plt.imsave(outfile, buf)

def create_spectrogram_from_folder(music_folder, out_folder):
    for filename in os.listdir(music_folder):
        if filename.endswith(".wav"):
            path_to_song = os.path.join(music_folder, filename)
            song = librosa.load(path_to_song, sr=22050, duration=5.0) # load 5 second slice of the song
            song_slices_folder = os.path.join(out_folder, os.path.splitext(filename)[0])

            if not os.path.exists(song_slices_folder):
                os.makedirs(song_slices_folder)

c_folder, output_folder)
