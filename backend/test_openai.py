from openai import OpenAI
import os
print("Key present:", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"Say hello in one sentence"}]
)
print(resp.choices[0].message.content)
