# #Step 1 : Setup Groq API key
# from dotenv import load_dotenv
# import os

# load_dotenv()
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# #Step 2 : Convert image to required format
# import base64
# image_path = "acne.jpg"
# image_file = open(image_path, "rb")
# encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
# # file being decoded to utf8 and encoded to base64


# def encode_image(image_path):
#     image_file = open(image_path, "rb")
#     return base64.b64encode(image_file.read()).decode('utf-8')


# #step 3 : Setup multimodal LLM
# from groq import Groq
# query = "Is there something wrong with my face"
# model = "meta-llama/llama-4-scout-17b-16e-instruct"
# # def analyze_image_with_query(query,model,encoded_image):
# #     client = Groq()

# #     messages=[
# #             {
# #                 "role": "user",
# #                 "content": [
# #                     {
# #                         "type": "text", 
# #                         "text": query
# #                     },
# #                     {
# #                         "type": "image_url",
# #                         "image_url": {
# #                             "url": f"data:image/jpeg;base64,{encoded_image}",
# #                         },
# #                     },
# #                 ],
# #             }]
# #     chat_completion=client.chat.completions.create(
# #         messages=messages,
# #         model=model
# #     )
# #     return chat_completion.choices[0].message.content
# def analyze_image_with_query(query, model, encoded_image):
#     client = Groq()

#     messages = [
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": query},
#                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
#             ],
#         }
#     ]

#     chat_completion = client.chat.completions.create(
#         messages=messages,
#         model=model
#     )

#     return chat_completion.choices[0].message.content

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

# Step 4: Run
# query = "Is there something wrong with my face?"
# model = "meta-llama/llama-4-scout-17b-16e-instruct"
# result = analyze_image_with_query(query, model, encoded_image)

# print("📝 Analysis Result:", result)

