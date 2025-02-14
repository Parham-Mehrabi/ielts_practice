from typing import Literal
from yapper import PiperSpeaker, PiperVoiceUK, PiperQuality

def get_speaker(speaker:Literal["cori", "alan", "british_female"]="cori"):
    speaker = speaker.lower()

    if speaker == "cori":
        return PiperSpeaker(voice=PiperVoiceUK.CORI)
    elif speaker == "alan":
        return PiperSpeaker(voice=PiperVoiceUK.ALAN)
    elif speaker == "british_female":
        return PiperSpeaker(voice=PiperVoiceUK.SOUTHERN_ENGLISH_FEMALE)



if __name__ == '__main__':
    get_speaker('alan').say(text=input("Enter the text: "))
