from PIL import Image
from music21 import stream, note

img = Image.open("photo.jpg").convert("L")

s = stream.Stream()

for pixel in list(img.getdata())[::500]:
    n = note.Note(60 + pixel // 15)
    s.append(n)

s.show("text")