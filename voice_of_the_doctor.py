# # Step 1a : Setup Text to speech-TTS-model for voice generation with gTTs
# import os
# from gtts import gTTS

# def text_to_speech_with_gtts_old(input_text,output_filepath):
#     language = 'en'

#     audioobj = gTTS(text=input_text, lang=language, slow=False)

#     audioobj.save(output_filepath)

# input_text = "Hello, I am the voice of the doctor. How can I assist you today?"
# # text_to_speech_with_gtts_old(input_text=input_text,output_filepath="gtts.testing.mp3")

# # Step 1b : Setup Text to speech-TTS-model for voice generation with ElevenLabs
# import elevenlabs
# from elevenlabs.client import ElevenLabs
# from dotenv import load_dotenv
# load_dotenv()
# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# def text_to_speech_with_elevenlabs_old(input_text,output_filepath):
#     client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio = client.generate(
#         text=input_text,
#         voice="Aria",
#         model="eleven_turbo_v2",
#         output_format="mp3_22050_32"
#     )
#     elevenlabs.save(audio, output_filepath)

# # text_to_speech_with_elevenlabs_old(input_text=input_text,output_filepath="elevenlabs.testing.mp3")
#     # Save the audio to a file


# # Step 2 : Use model for text output to voice
# # for auto playing the audio we use subprocess library to play the audio file
# import subprocess
# import platform
# from gtts import gTTS
# def text_to_speech_with_gtts(input_text,output_filepath):
#     language = 'en'

#     audioobj = gTTS(text=input_text, lang=language, slow=False)

#     audioobj.save(output_filepath)
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['start', output_filepath],shell=True)
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['mpg123', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")

# input_text = "Hello, I am sidhant singh bhadauriya. How can I assist you today?"
# # text_to_speech_with_gtts(input_text=input_text,output_filepath="gtts_testing_autoplaying.mp3")



# def text_to_speech_with_elevenlabs(input_text,output_filepath):
#     client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio = client.generate(
#         text=input_text,
#         voice="Aria",
#         model="eleven_turbo_v2",
#         output_format="mp3_22050_32"
#     )
#     elevenlabs.save(audio, output_filepath)
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['start', output_filepath],shell=True)
#             # subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")

# text_to_speech_with_elevenlabs(input_text=input_text,output_filepath="elevenlabs_testing_autoplaying.mp3")

import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath):
    language = 'en'
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        model="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )
    elevenlabs.save(audio, output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
