# Default
import os

from groq import Groq


client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("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"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="gemma2-9b-it",
)

print(chat_completion.choices[0].message.content)