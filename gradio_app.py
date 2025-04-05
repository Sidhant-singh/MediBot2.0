# this is UI
# import gradio as gr
# from brain_of_the_doctor import analyze_image_with_query
# from voice_of_the_patient import transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts
# import os
# from dotenv import load_dotenv
# import base64

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# # Store chat history
# chat_history = []

# system_prompt = """You are a professional doctor providing medical assistance. 
# Remember previous messages in the conversation and respond accordingly. Keep responses concise (max 2 sentences)."""

# # Encode image to base64
# def encode_image(image_filepath):
#     with open(image_filepath, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# def chat_with_doctor(audio_filepath, image_filepath):
#     global chat_history

#     if not audio_filepath:
#         return chat_history, None, "No speech detected, please try again."

#     user_input = transcribe_with_groq(audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY, stt_model="whisper-large-v3")
#     if not user_input:
#         return chat_history, None, "Couldn't process speech. Please try again."

#     chat_history.append(("User", user_input))

#     formatted_history = "\n".join([f"{role}: {message}" for role, message in chat_history])
#     full_prompt = f"{system_prompt}\n\nChat History:\n{formatted_history}\n\nDoctor:"
    
#     print(f"Query Sent to LLM: {full_prompt}")

#     if image_filepath:
#         encoded_img = encode_image(image_filepath)
#         doctor_response = analyze_image_with_query(query=full_prompt, encoded_image=encoded_img, model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = analyze_image_with_query(query=full_prompt, model="llama-3.2-11b")

#     if not doctor_response:
#         return chat_history, None, "Error processing response. Try again."

#     chat_history.append(("Doctor", doctor_response))

#     output_audio = "final.mp3"
#     text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio)

#     print(f"Generated Speech File: {output_audio}")

#     return chat_history, output_audio, "Response ready!"

# def clear_conversation():
#     global chat_history
#     chat_history = []
#     return [], None, ""

# # Using Enhanced CSS File
# with gr.Blocks(css="style.css") as iface:
#     # Header
#     gr.HTML("""
#     <div class="header-container">
#         <h1>👨‍⚕️ MediBot 2.0</h1>
#         <div class="subtitle">Your AI Medical Assistant - Speak to get professional medical insights</div>
#     </div>
#     """)
    
#     with gr.Row():
#         with gr.Column():
#             # Voice Input Section
#             with gr.Group(elem_classes="input-section"):
#                 gr.Markdown("## 🎙️ Voice Input")
#                 voice_input = gr.Audio(sources=["microphone"], type="filepath", label="Speak your medical question")
            
#             # Image Upload Section
#             with gr.Group(elem_classes="input-section"):
#                 gr.Markdown("## 📸 Image Upload")
#                 image_input = gr.Image(type="filepath", label="Upload a relevant medical image (optional)")
            
#             # Buttons
#             with gr.Row():
#                 submit_btn = gr.Button("🚀 Submit", elem_classes="gr-button")
#                 clear_btn = gr.Button("🗑️ Reset", elem_classes="gr-button clear-button")
                
#         with gr.Column():
#             # Conversation Section
#             with gr.Group(elem_classes="output-section"):
#                 gr.Markdown("## 💬 Conversation")
#                 chat_output = gr.Chatbot(elem_classes="chatbot-container")
                
#             # Voice Response Section
#             with gr.Group(elem_classes="output-section"):
#                 gr.Markdown("## 🔊 Doctor's Voice Response")
#                 audio_output = gr.Audio(label="Listen to response")
#                 status_text = gr.Textbox(label="Status", lines=1)

#     # Footer
#     gr.HTML("""
#     <div class="footer">
#         <p>MediBot 2.0 is designed for educational purposes. Always consult with a real healthcare professional for medical advice.</p>
#         <p>© 2025 MediBot Health Solutions</p>
#     </div>
#     """)
            
#     submit_btn.click(fn=chat_with_doctor, inputs=[voice_input, image_input], outputs=[chat_output, audio_output, status_text])
#     clear_btn.click(fn=clear_conversation, inputs=[], outputs=[chat_output, audio_output, status_text])

# iface.launch(debug=True)
# import gradio as gr
# from brain_of_the_doctor import analyze_image_with_query
# from voice_of_the_patient import transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts
# import os
# from dotenv import load_dotenv
# import base64

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# # Store chat history
# chat_history = []

# system_prompt = """You are a professional doctor providing medical assistance. 
# Remember previous messages in the conversation and respond accordingly. Keep responses concise (max 2 sentences)."""

# def encode_image(image_filepath):
#     """Encodes an image to a base64 string for processing."""
#     with open(image_filepath, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# def chat_with_doctor(audio_filepath, image_filepath):
#     global chat_history

#     if not audio_filepath:
#         return chat_history, "No speech detected, please try again.", None

#     user_input = transcribe_with_groq(audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY, stt_model="whisper-large-v3")
#     if not user_input:
#         return chat_history, "Couldn't process speech. Please try again.", None

#     chat_history.append(("User", user_input))

#     formatted_history = "\n".join([f"{role}: {message}" for role, message in chat_history])
#     full_prompt = f"{system_prompt}\n\nChat History:\n{formatted_history}\n\nDoctor:"
    
#     print(f"Query Sent to LLM: {full_prompt}")  # Debugging
    
#     if image_filepath:
#         encoded_img = encode_image(image_filepath)
#         doctor_response = analyze_image_with_query(query=full_prompt, encoded_image=encoded_img, model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = analyze_image_with_query(query=full_prompt, model="llama-3.2-11b")

#     if not doctor_response:
#         return chat_history, "Error processing response. Try again.", None

#     chat_history.append(("Doctor", doctor_response))

#     output_audio = "final.mp3"
#     text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio)
    
#     print(f"Generated Speech File: {output_audio}")  # Debugging

#     return chat_history, output_audio

# def clear_conversation():
#     global chat_history
#     chat_history = []
#     return [], None, None  # Clear chat, image, and audio

# def download_chat():
#     """Generate a text file of the chat history and provide a download link."""
#     chat_text = "\n".join([f"{role}: {message}" for role, message in chat_history])
#     filename = "chat_history.txt"
    
#     with open(filename, "w", encoding="utf-8") as file:
#         file.write(chat_text)
    
#     return filename

# # Define Gradio UI with updated inline CSS
# custom_css = """
# <style>
#     body {
#         background-color: #e6f7ff;
#         font-family: 'Poppins', 'Arial', sans-serif;
#         margin: 0;
#         padding: 0;
#     }
#     .gradio-container {
#         background: linear-gradient(to bottom right, #ffffff, #f0f8ff);
#         border-radius: 16px;
#         padding: 25px;
#         box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
#         max-width: 1000px;
#         margin: 20px auto;
#         border: 1px solid #d1e6ff;
#     }
#     .header-container {
#         background: linear-gradient(135deg, #4da6ff, #0066cc);
#         padding: 20px;
#         border-radius: 12px;
#         margin-bottom: 25px;
#         text-align: center;
#         box-shadow: 0 4px 12px rgba(29, 86, 163, 0.2);
#     }
#     h1 {
#         color: white;
#         font-weight: 700;
#         margin: 0;
#         padding: 10px 0;
#         font-size: 34px;
#         text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
#     }
    
#     /* Red buttons with hover effect */
#     button {
#         background: #e60000;
#         color: white;
#         font-size: 16px;
#         font-weight: 600;
#         border-radius: 8px;
#         padding: 12px 24px;
#         border: none;
#         cursor: pointer;
#         box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
#         transition: all 0.3s ease;
#         margin-right: 10px;
#     }
#     button:hover {
#         background: #cc0000;
#         box-shadow: 0 4px 10px rgba(230, 0, 0, 0.4);
#         transform: translateY(-3px);
#     }
    
#     /* Audio recording and image upload styles */
#     .input-container {
#         background-color: #d1e9ff;
#         border-radius: 12px;
#         padding: 15px;
#         margin-bottom: 20px;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
#         border: 2px solid #a0cfff;
#     }
#     .input-container label {
#         font-weight: 800;
#         color: #001f33;
#         font-size: 18px;
#         margin-bottom: 10px;
#         display: block;
#     }
    
#     /* Conversation history styling */
#     .chatbot-container {
#         background-color: #fffbe6;
#         border-radius: 12px;
#         padding: 20px;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
#         margin-top: 20px;
#         border: 2px solid #fff2b3;
#     }
#     .chatbot-container .message {
#         padding: 14px;
#         border-radius: 10px;
#         margin: 10px 0;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
#     }
#     .chatbot-container .user-message {
#         background-color: #e6f0ff;
#         border-left: 5px solid #3399ff;
#     }
#     .chatbot-container .bot-message {
#         background-color: #f0f9e6;
#         border-left: 5px solid #66cc33;
#     }
    
#     /* Image display enhancement */
#     .image-preview {
#         border: 3px solid #99ccff;
#         border-radius: 10px;
#         overflow: hidden;
#         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
#         transition: all 0.3s ease;
#     }
#     .image-preview:hover {
#         transform: scale(1.02);
#         box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
#     }
    
#     /* Audio output styling */
#     .audio-output {
#         background-color: #e6f7ff;
#         border-radius: 12px;
#         padding: 15px;
#         margin-top: 20px;
#         border: 2px solid #b3e0ff;
#     }
#     .audio-output label {
#         font-weight: 700;
#         color: #003366;
#         font-size: 18px;
#     }
# </style>
# """import gradio as gr
from brain_of_the_doctor import analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts
import os
import base64
from dotenv import load_dotenv

load_dotenv()

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
        doctor_response = analyze_image_with_query(query=full_prompt, encoded_image=encoded_img, model="llama-3.2-11b-vision-preview")
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
import gradio as gr
with gr.Blocks() as iface:
    gr.HTML(custom_css)
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

iface.launch(debug=True)
