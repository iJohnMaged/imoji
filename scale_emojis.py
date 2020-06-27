import os
from PIL import Image

for file in os.listdir("emojis/"):
    if file.endswith(".png"):
        print(os.path.join("emojis/", file))
        image = Image.open(os.path.join("emojis/", file)).convert('RGBA')
        image = image.resize((36, 36))
        image.save(os.path.join("resized_emojis/", file))