import json
import whisper

whispher_model = whisper.load_model("base")

with open("config.json", "r") as configFIle:
     configData = json.load(configFIle)