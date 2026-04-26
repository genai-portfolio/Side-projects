import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="meta-llama/Llama-3.2-1B-Instruct",
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)


response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}]
)

