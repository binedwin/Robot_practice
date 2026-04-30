import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
response = client.responses.create(
    model = "gpt-5-nano",
    input = "오늘 점심 메뉴 추천해줘"
)

print (response.output_text)