from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyAALKB6MTzyiLr9rnfkkqJQkoKU5Z8GILg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain to me how AI works"},
    ],
)

print(response.choices[0].message)
