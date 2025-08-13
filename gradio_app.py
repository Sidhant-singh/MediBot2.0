# from brain_of_the_doctor import analyze_image_with_query
# from voice_of_the_patient import transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Step 1: Setup Groq API key
from dotenv import load_dotenv
import os
import base64
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

# Step 2: Encode image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "acne.jpg"
encoded_image = encode_image(image_path)

# Step 3: Analyze image with query
def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content












import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from dotenv import load_dotenv
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    audio_file = open(audio_filepath, "rb")
    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en",
    )
    return transcription.text








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






GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

chat_history = []

system_prompt = """You are a professional doctor providing medical assistance. 
Remember previous messages in the conversation and respond accordingly. Keep responses concise (max 2 sentences)."""

def encode_image(image_filepath):
    with open(image_filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat_with_doctor(audio_filepath, image_filepath):
    global chat_history

    if not audio_filepath:
        return chat_history, "No speech detected, please try again.", None

    user_input = transcribe_with_groq(audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY, stt_model="whisper-large-v3")
    if not user_input:
        return chat_history, "Couldn't process speech. Please try again.", None

    chat_history.append(("User", user_input))

    formatted_history = "\n".join([f"{role}: {message}" for role, message in chat_history])
    full_prompt = f"{system_prompt}\n\nChat History:\n{formatted_history}\n\nDoctor:"
    
    print(f"Query Sent to LLM: {full_prompt}")
    
    if image_filepath:
        encoded_img = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(query=full_prompt, encoded_image=encoded_img, model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = analyze_image_with_query(query=full_prompt, model="llama-3.2-11b")

    if not doctor_response:
        return chat_history, "Error processing response. Try again.", None

    chat_history.append(("Doctor", doctor_response))

    output_audio = "final.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio)
    
    print(f"Generated Speech File: {output_audio}")

    return chat_history, output_audio

def clear_conversation():
    global chat_history
    chat_history = []
    return [], None, None

def download_chat():
    chat_text = "\n".join([f"{role}: {message}" for role, message in chat_history])
    filename = "chat_history.txt"
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(chat_text)
    
    return filename

custom_css = """
<style>
    body {
        background-color: #e6f7ff;
        font-family: 'Poppins', 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .gradio-container {
        background: linear-gradient(to bottom right, #ffffff, #f0f8ff);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        max-width: 1000px;
        margin: 20px auto;
        border: 1px solid #d1e6ff;
    }
    .header-container {
        background: linear-gradient(135deg, #4da6ff, #0066cc);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(29, 86, 163, 0.2);
    }
    h1 {
        color: white;
        font-weight: 700;
        margin: 0;
        padding: 10px 0;
        font-size: 34px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    .red-button {
        background: #ff6666; /* Light red */
        color: white;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        margin-right: 10px;
    }

    .red-button:hover {
        background: #ff4d4d; /* Slightly darker red on hover */
        box-shadow: 0 4px 10px rgba(255, 102, 102, 0.4);
        transform: translateY(-3px);
    }
    button {
        background: #74B1EA; /* Light blue */
        color: white;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        margin-right: 10px;
    }
    button:hover {
        background: #559FE5;
        box-shadow: 0 4px 10px rgba(230, 0, 0, 0.4);
        transform: translateY(-3px);
    }
    .input-container {
        background-color: #d1e9ff;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 2px solid #a0cfff;
    }
    .chatbot-container {
        background-color: #fffbe6;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        border: 2px solid #fff2b3;
    }
    

</style>
"""
# import gradio as gr
# with gr.Blocks() as iface:
#     gr.HTML(custom_css)
#     gr.Markdown("# 🏥 MediBot 2.0 - AI Medical Assistant")
#     gr.Markdown("## Speak your medical questions and upload relevant images for analysis.")

#     with gr.Row():
#         with gr.Column(elem_classes="input-container"):
#             voice_input = gr.Audio(type="filepath", label="🎤 Speak Your Medical Question")
        
#         with gr.Column(elem_classes="input-container"):
#             image_input = gr.Image(type="filepath", label="📸 Upload Medical Image (Optional)")
    
#     with gr.Row():
#         submit_btn = gr.Button("Submit", elem_classes="red-button")
#         clear_btn = gr.Button("Clear Chat & Image", elem_classes="red-button")
#         download_btn = gr.Button("📥 Download Chat", elem_classes="red-button")

    
#     chat_output = gr.Chatbot(label="💬 Conversation History", elem_classes="chatbot-container")
    
#     with gr.Row():
#         audio_output = gr.Audio(label="🔊 Doctor's Response")
    
#     download_file = gr.File(label="Download Chat History")

#     submit_btn.click(fn=chat_with_doctor, inputs=[voice_input, image_input], outputs=[chat_output, audio_output])
#     clear_btn.click(fn=clear_conversation, inputs=[], outputs=[chat_output, image_input, audio_output])
#     download_btn.click(fn=download_chat, inputs=[], outputs=[download_file])

# iface.launch(debug=True)

with gr.Blocks(css=custom_css) as iface:
    gr.Markdown("# 🏥 MediBot 2.0 - AI Medical Assistant")
    gr.Markdown("## Speak your medical questions and upload relevant images for analysis.")

    with gr.Row():
        with gr.Column(elem_classes="input-container"):
            voice_input = gr.Audio(type="filepath", label="🎤 Speak Your Medical Question")
        with gr.Column(elem_classes="input-container"):
            image_input = gr.Image(type="filepath", label="📸 Upload Medical Image (Optional)")
    
    with gr.Row():
        submit_btn = gr.Button("Submit", elem_classes="red-button")
        clear_btn = gr.Button("Clear Chat & Image", elem_classes="red-button")
        download_btn = gr.Button("📥 Download Chat", elem_classes="red-button")

    chat_output = gr.Chatbot(label="💬 Conversation History", elem_classes="chatbot-container")

    with gr.Row():
        audio_output = gr.Audio(label="🔊 Doctor's Response")

    download_file = gr.File(label="Download Chat History")

    submit_btn.click(fn=chat_with_doctor, inputs=[voice_input, image_input], outputs=[chat_output, audio_output])
    clear_btn.click(fn=clear_conversation, inputs=[], outputs=[chat_output, image_input, audio_output])
    download_btn.click(fn=download_chat, inputs=[], outputs=[download_file])

# Launch with Render-compatible settings
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    iface.launch(server_name="0.0.0.0", server_port=port, debug=True)