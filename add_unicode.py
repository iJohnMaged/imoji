import json

with open("emojis_data/colors_emojis_mean.json") as f:
    emojis_data = json.load(f)

output = []
for emoji in emojis_data:
    emoji_file = emoji[0]
    # get unicode part
    unicodes = emoji_file.split(".png")[0].split("_", 1)[-1].replace("_", "-").split("-")
    print(unicodes)
    str_ = ""
    for uc in unicodes:
        str_ += f"\\U{(uc.rjust(8, '0').upper())}"
    emoji.append(str_.encode("utf-8").decode('unicode-escape'))
    print(unicodes, emoji)
    output.append(emoji)

# with open("emojis_data/colors_emojis_mean_unicode.json", "w") as f:
#     json.dump(output, f)