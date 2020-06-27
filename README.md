# Imoji 📷
A little script that turns images to emojis using python 3! Imoji!

Script saves the imoji inside output folder, as well as save a text version in output_emoji.txt file.

# Installation and usage
* Install requirements

`pip install -r requirements.text`

* Run script

`python3 imojy.py -i input_img.jpg`

# Script arguments

| argument         | description                                   | required | default                |
| ---------------- | --------------------------------------------- | -------- | ---------------------- |
| -i --input       | Input image                                   | ✅        | None                   |
| -s --scale       | Divides the original image size by that scale | ❌        | 15                     |
| -m --mirror      | Add the original image next to the imoji      | ❌        | False                  |
| -o --open        | opens the image after saving it               | ❌        | False                  |
| -bg --background | Color for background ex: black, white, red    | ❌        | transparent background |
