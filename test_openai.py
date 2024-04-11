# import openai

key = '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'
# chat_sp.api_key = key

# completion = chat_sp.Completion.create(
#     engine="gpt-3.5-turbo",
#     prompt="Compose a poem that explains the concept of recursion in programming.",
#     max_tokens=100
# )

# messages = [
#     {"role":"system",
#      "content":"you are a kind helpful assistant"},
#     {
#      "role":"user",
#      "content":"virat kohli"
#     }
# ]

# chat = openai.ChatCompletion.create(
#     model = "gpt-3.5-turbo",
#     messages = messages
# )


# reply = chat.choices[0].messages.content
# print(reply)

# # print(completion["choices"][0]["text"])


# setx OPENAI_API_KEY "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"
from openai import OpenAI
import openai
client = OpenAI()
client = openai.Client(api_key=key)
# setx OPENAI_API_KEY "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"
# openai.api_key = key

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "you are a kind helpful assistant"},
    {"role": "user", "content": "virat kohli"}
  ]
)

print(completion.choices[0].message.content)
