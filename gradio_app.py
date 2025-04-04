# #VoiceBot UI Gradio App
# import gradio as gr
# from brain_of_the_doctor import encode_image,analyze_image_with_query
# from voice_of_the_patient import record_audio,transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts , text_to_speech_with_elevenlabs

# from dotenv import load_dotenv
# load_dotenv()
# import os

# system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
#             What's in this image?. Do you find anything wrong with it medically? 
#             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
#             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
#             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
#             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
#             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


# def process_inputs(audio_filepath, image_filepath):
#     speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.getenv("GROQ_API_KEY"), 
#                                                  audio_filepath=audio_filepath,
#                                                  stt_model="whisper-large-v3")


#     # Handle the image input
#     if image_filepath:
#         doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = "No image provided for me to analyze"

#     voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3") 

#     return speech_to_text_output, doctor_response, voice_of_doctor

# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath"),
#         gr.Image(type="filepath")
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio("Temp.mp3")
#     ],
#     title="MediBot 2.0"
# )

# iface.launch(debug=True)
import gradio as gr
from brain_of_the_doctor import analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# Store chat history
chat_history = []

system_prompt = """You are a professional doctor providing medical assistance. 
Remember previous messages in the conversation and respond accordingly. Keep responses concise (max 2 sentences)."""

import base64

def encode_image(image_filepath):
    """Encodes an image to a base64 string for processing."""
    with open(image_filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat_with_doctor(audio_filepath, image_filepath):
    global chat_history

    # Ensure audio input exists
    if not audio_filepath:
        return chat_history, "No speech detected, please try again.", None

    # Convert speech to text
    user_input = transcribe_with_groq(audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY, stt_model="whisper-large-v3")
    # user_input = transcribe_with_groq(audio_filepath,GROQ_API_KEY,stt_model="whisper-large-v3")
    if not user_input:
        return chat_history, "Couldn't process speech. Please try again.", None

    chat_history.append(("User", user_input))

    # Prepare context-aware prompt
    formatted_history = "\n".join([f"{role}: {message}" for role, message in chat_history])
    full_prompt = f"{system_prompt}\n\nChat History:\n{formatted_history}\n\nDoctor:"
    
    print(f"Query Sent to LLM: {full_prompt}")  # Debugging
    
    # Process image if provided
    if image_filepath:
        encoded_img = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(query=full_prompt, encoded_image=encoded_img, model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = analyze_image_with_query(query=full_prompt, model="llama-3.2-11b")

    if not doctor_response:
        return chat_history, "Error processing response. Try again.", None

    # Append doctor's response
    chat_history.append(("Doctor", doctor_response))

    # Convert response to speech
    output_audio = "final.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio)
    
    print(f"Generated Speech File: {output_audio}")  # Debugging

    return chat_history, output_audio

def clear_conversation():
    global chat_history
    chat_history = []
    return [], None, None  # Clear chat, image, and audio

# Define Gradio UI
with gr.Blocks() as iface:
    gr.Markdown("# 🏥 MediBot 2.0 - AI Medical Assistant")
    gr.Markdown("Speak your medical questions and upload relevant images for analysis.")

    with gr.Row():
        voice_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak your medical question")
        image_input = gr.Image(type="filepath", label="📸 Upload Medical Image (Optional)")
    
    submit_btn = gr.Button("Submit")
    clear_btn = gr.Button("Clear Chat & Image")

    chat_output = gr.Chatbot(label="💬 Conversation History")
    audio_output = gr.Audio(label="🔊 Doctor's Response")

    submit_btn.click(fn=chat_with_doctor, inputs=[voice_input, image_input], outputs=[chat_output, audio_output])
    clear_btn.click(fn=clear_conversation, inputs=[], outputs=[chat_output, image_input, audio_output])

iface.launch(debug=True)
