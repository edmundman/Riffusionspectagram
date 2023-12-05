import os
import sys
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm 

def create_save_spectrogram(song, song_name, folder):
    plt.interactive(False)
    clip, sample_rate = librosa.load(song, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.specgram(clip, NFFT=512, Fs=2, Fc=0, noverlap=128, cmap='inferno', mode='psd')
    ax.axis('off')
    ax.grid(False)
    ax.set_frame_on(False)
    fig.canvas.draw()
    buf = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
    buf = buf.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    buf = np.array(buf)
    plt.close(fig)
    buf = buf.astype(np.float32)/255.

    filename = os.path.splitext(os.path.basename(song_name))[0]
    outfile = os.path.join(folder, "{}.png".format(filename))
    plt.imsave(outfile, buf)

def create_spectrogram_from_folder(music_folder, out_folder):
    wav_files = [f for f in os.listdir(music_folder) if f.endswith('.wav')]
    
    for filename in tqdm(wav_files, desc='Processing', colour='blue'):
        path_to_song = os.path.join(music_folder, filename)
        song = librosa.load(path_to_song, sr=22050, duration=5.0)
        song_slices_folder = os.path.join(out_folder, os.path.splitext(filename)[0])

        if not os.path.exists(song_slices_folder):
            os.makedirs(song_slices_folder)

        create_save_spectrogram(path_to_song, filename, song_slices_folder)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python spectrogram_generator.py <path_to_music_folder> <path_to_output_folder>")
        sys.exit(1)

    music_folder = sys.argv[1]
    output_folder = sys.argv[2]

    create_spectrogram_from_folder(music_folder, output_folder)
