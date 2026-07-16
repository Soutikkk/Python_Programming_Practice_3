import sounddevice as sd
from scipy.io.wavfile import write

sec = int(input("Record seconds: "))
fs = 44100

print("Recording...")

audio = sd.rec(
    int(sec * fs),
    samplerate=fs,
    channels=2,
    dtype="int16"
)

sd.wait()

write("record.wav", fs, audio)

print("Saved record.wav")